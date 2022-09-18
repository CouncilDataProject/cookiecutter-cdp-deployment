import React from "react";
import ReactDOM from "react-dom";
import { App, AppConfigProvider } from "@councildataproject/cdp-frontend";

import "@councildataproject/cdp-frontend/dist/index.css";

const config = {
    firebaseConfig: {
        options: {
            projectId: "{{ cookiecutter.infrastructure_slug }}",
        },
        settings: {},
    },
    municipality: {
        name: "{{ cookiecutter.municipality }}",
        timeZone: "{{ cookiecutter.iana_timezone }}",
        footerLinksSections: [],
    },
    features: {
        enableClipping: {{ cookiecutter.enable_clipping }},
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