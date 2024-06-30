# In a file called [project root]/components/card/card.py
from django_components import component


@component.register("card")
class Card(component.Component):
    # Templates inside `[your apps]/components` dir and `[project root]/components` dir will be automatically found. To customize which template to use based on context
    # you can override def get_template_name() instead of specifying the below variable.
    template_name = "card/template.html"

    # This component takes one parameter, a title string to show in the template
    def get_context_data(self, comics):
        context = {
            "comics": comics,
        }
        return context

    # class Media:
    #     css = "card/style.css"
    #     js = "card/script.js"
