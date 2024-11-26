import App from './app.js';
import Bitrix24 from './bitrix24.js';


document.addEventListener("DOMContentLoaded", () => {
    BX24.ready(function() {
        const container = document.querySelector("#containerEventsManagement");
        const apiClient = Bitrix24();
        const app = new App(container, apiClient);

        app.init();
    })
})
