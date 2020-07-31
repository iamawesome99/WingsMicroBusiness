from django.db import models
import ast
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify
import logging

logger = logging.getLogger(__name__)


def get_image_filename(instance, filename):
    title = instance.product.name
    slug = slugify(title)
    return "post_images/%s-%s" % (slug, filename)


def parse_options(value):

    choice_list = []

    for i in value.split("||"):

        choice_text = i.split("|")

        name = choice_text[0]
        choices = [x.split(":")[0] for x in choice_text[1:]]
        prices = [int(x.split(":")[1]) for x in choice_text[1:]]

        choice_list.append(Choice(name, choices, prices))

    return Options(choice_list)


class Choice:

    def __init__(self, name, choices, del_price):
        self.choices = choices
        self.del_price = del_price
        self.name = name

    def __str__(self):
        return str(self.name) + "|" + "|".join([str(c) + ":" + str(p) for c, p in zip(self.choices, self.del_price)])

    def choose(self, choice):
        try:
            return self.del_price[choice]
        except IndexError:
            raise IndexError("Choice is not present.")

    def reverse_choose(self, choice):
        for count, i in enumerate(self.choices):
            print(i, count, choice)
            if i == choice:
                return self.del_price[count]
        raise IndexError("Choice is not present.")


class Options:

    def __init__(self, options):
        self.options = options

    def __str__(self):
        return "||".join([str(c) for c in self.options])

    def choose(self, choices):

        del_price = 0

        for c, o in zip(choices, self.options):
            del_price += o.choose(c)

        return del_price

    def dict_choose(self, choices):

        del_price = 0

        for k, v in choices.items():
            for i in self.options:
                if i.name == k:
                    del_price += i.reverse_choose(v)
                    break

        return del_price

    # Removes all choices from the choices dict that aren't
    def remove_non_choices(self, choices):
        allowed = [i.name for i in self.options]
        for k, _ in choices.copy().items():
            if k not in allowed:
                del choices[k]
        return choices


class SpecificProduct:

    def __init__(self, product, selected_options, quantity=None):
        self.product = product

        print(selected_options)

        if quantity:
            self.quantity = quantity
        else:
            self.quantity = int(selected_options["quantity"])

        self.selected_options = product.options.remove_non_choices(selected_options)

        self.price = (product.options.dict_choose(selected_options) + product.base_price) * self.quantity

    def __str__(self):
        return self.product.name + " Options: " + \
               "".join([str(k) + ": " + str(v) + " | " for k, v in self.selected_options.items()])

    def encode(self):
        return str(self.product.id) + "|" + str(self.quantity) + "|" + str(self.selected_options)

    def is_same_product(self, other):
        return self.product.id == other.product.id and str(self.selected_options) == str(other.selected_options)

    @staticmethod
    def decode(encoded):
        encoded = encoded.split('|')
        product = get_object_or_404(Product, pk=encoded[0])
        quantity = int(encoded[1])
        selected_options = ast.literal_eval(encoded[2])
        return SpecificProduct(product, selected_options, quantity=quantity)


class OptionsField(models.Field):

    def db_type(self, connection):
        return "CHAR(500)"

    def from_db_value(self, value, expression, connection):
        return parse_options(value)

    def to_python(self, value):

        if isinstance(value, Choice):
            return value

        return parse_options(value)

    def get_prep_value(self, value):
        return str(value)


class Branch(models.Model):

    name = models.CharField(max_length=200, default="branch_name")
    display_name = models.CharField(max_length=200, default="Branch Name")

    header_background_color = models.CharField(max_length=20, default="white")
    header_text_color = models.CharField(max_length=20, default="black")
    background_color = models.CharField(max_length=20, default="white")

    logo = models.ImageField(upload_to="logos")
    icon = models.ImageField(upload_to="icons")

    def __str__(self):
        return self.display_name


class Product(models.Model):

    name = models.CharField(max_length=200)
    description = models.TextField()
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)

    other_branches = models.ManyToManyField(Branch, related_name="other_branch", blank=True)

    base_price = models.IntegerField(default=0)

    options = OptionsField(blank=True)

    def __str__(self):
        return self.name

    def get_main_image(self):
        try:
            return ProductImage.objects.get(product=self, is_main_image=True)
        except ProductImage.DoesNotExist:
            logger.error("Unable to find a main image for product " + str(self))
        except ProductImage.MultipleObjectsReturned:
            logger.error("Found multiple main images for product " + str(self))


class ProductImage(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    caption = models.CharField(max_length=500, default="")
    image = models.ImageField(upload_to=get_image_filename,
                              verbose_name='Image')

    is_main_image = models.BooleanField(default=False)

    def __str__(self):
        return self.caption

