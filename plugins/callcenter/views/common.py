from flask_appbuilder import BaseView, expose


class ExtensionAgentView(BaseView):
    default_view = 'list'

    @expose('/')
    def list(self):
        return self.render_template(
            template="callcenter/templates/extension_agent.html",
            custom_message="Hello from extension agent"
        )


class ExtensionGroupView(BaseView):
    default_view = 'list'

    @expose('/')
    def list(self):
        return self.render_template(
            template="callcenter/templates/extension_group.html",
            custom_message="Hello from extension group"
        )