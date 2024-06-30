# In a file called [project root]/components/table/table.py
from django_components import component


@component.register("table")
class Table(component.Component):
    # Templates inside `[your apps]/components` dir and `[project root]/components` dir will be automatically found. To customize which template to use based on context
    # you can override def get_template_name() instead of specifying the below variable.
    template_name = "table/template.html"

    # This component takes one parameter, a title string to show in the template
    def get_context_data(
        self,
        table,
    ):
        context = {
            "table": table,
        }
        return context

    # class Media:
    #     css = "table/style.css"
    #     js = "table/script.js"
