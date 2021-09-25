import React from "react";
import ReactDOM from "react-dom";
import { App, AppConfigProvider } from "@councildataproject/cdp-frontend";

ReactDOM.render(
    <div>
        <AppConfigProvider
            appConfig={{
                firebaseConfig: {
                    options: {
                        projectId: "{{ cookiecutter.infrastructure_slug }}",
                    },
                    settings: {},
                },
                municipality: {
                    name: "{{ cookiecutter.municipality_name }}",
                    footerLinksSections: [],
                },
            }}
        >
            <App />
        </AppConfigProvider>
    </div>,
    document.getElementById("root")
);
