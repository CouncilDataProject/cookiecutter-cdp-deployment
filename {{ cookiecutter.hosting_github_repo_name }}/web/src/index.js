{% raw %}
import React from "react";
import ReactDOM from "react-dom";
import { App, AppConfigProvider } from "@councildataproject/cdp-frontend";

ReactDOM.render(
    <div>
        <AppConfigProvider
            appConfig={{
                firebaseConfig: {
                    options: {
                        projectId: {% endraw %}"{{ cookiecutter.infrastructure_slug }}"{% raw %},
                    },
                    settings: {},
                },
                municipality: {
                    name: {% endraw %}"{{ cookiecutter.municipality_name }}"{% raw %},
                    footerLinksSections: [],
                },
            }}
        >
            <App />
        </AppConfigProvider>
    </div>,
    document.getElementById("root")
);
{% endraw %}