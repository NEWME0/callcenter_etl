from flask_admin import BaseView, expose


class ExtensionAgentView(BaseView):
    @expose('/')
    def index(self):
        return self.render(
            "callcenter/common/templates/extension_agent.html",
            content={
                "custom_message": "Hello from extension agent"
            }
        )


class ExtensionGroupView(BaseView):
    @expose('/')
    def index(self):
        return self.render(
            "callcenter/common/templates/extension_group.html",
            content={
                "custom_message": "Hello from extension group"
            }
        )


extension_agent_view = ExtensionAgentView(category='Key Way Group', name='Extension agent')
extension_group_view = ExtensionGroupView(category='Key Way Group', name='Extension group')
