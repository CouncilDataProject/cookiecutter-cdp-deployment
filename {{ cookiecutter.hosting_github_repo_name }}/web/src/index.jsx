import React from "react";
import ReactDOM from "react-dom";
import { App, AppConfigProvider } from "@councildataproject/cdp-frontend";

import "@councildataproject/cdp-design/dist/images.css";
import "@councildataproject/cdp-design/dist/colors.css";
import "@mozilla-protocol/core/protocol/css/protocol.css";
import "@mozilla-protocol/core/protocol/css/protocol-components.css";
import "semantic-ui-css/semantic.min.css";

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