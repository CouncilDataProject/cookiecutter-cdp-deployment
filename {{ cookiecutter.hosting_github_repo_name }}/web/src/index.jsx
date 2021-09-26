import React from "react";
import ReactDOM from "react-dom";
import { App, AppConfigProvider } from "@councildataproject/cdp-frontend";

const config = {
    firebaseConfig: {
        options: {
            projectId: "{{ cookiecutter.infrastructure_slug }}",
        },
        settings: {},
    },
    municipality: {
        name: "{{ cookiecutter.municipality }}",
        footerLinksSections: [],
    },
}

ReactDOM.render(
    <div>
        <AppConfigProvider appConfig={config}>
            <App />
        </AppConfigProvider>
    </div>,
    document.getElementById("root")
);