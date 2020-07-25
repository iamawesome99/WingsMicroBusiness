from django import forms


class OptionsForm(forms.Form):

    def __init__(self, opts, *args, **kwargs):
        super(OptionsForm, self).__init__(*args, **kwargs)

        for i in opts.options:
            c = [(x, x) for x, y in zip(i.choices, i.del_price)]

            self.fields[i.name] = forms.ChoiceField(choices=c, widget=forms.RadioSelect)
