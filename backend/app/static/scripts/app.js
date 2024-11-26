import Templates from "./templates.js";


export default class App {
    constructor(container, apiClient) {
        this.container = container;
        this.apiClient = apiClient;

        this.eventsList = [];
    }

    async init() {
        this.eventsList = await this.apiClient.callMethod("events", {});
        await this.render();

        this.elemSelectTypeEvent = this.container.querySelector(".bx24_events__type_event select");
        this.elemSelectNameEvent = this.container.querySelector(".bx24_events__name_event select");
        this.elemInputHandlerEvent = this.container.querySelector(".bx24_events__handler_event input");
        this.elemInputSourceEvent = this.container.querySelector(".bx24_events__source_event input");
        this.btnAddEvent = this.container.querySelector(".bx24_events__add_event button");
        this.setOfflineEvent(this.elemSelectTypeEvent.value)

        this.initHandler();
        BX24.fitWindow();
    }

    initHandler() {
        // Удаление зарегистрированного события
        this.container.addEventListener("click", async (e) => {
            let elemRemoveEvent = e.target.classList.contains("bx24_events__table_events_remove_row_i");
            let elemTr = e.target.closest("tr");
            if (elemRemoveEvent && elemTr) {
                let isRemoveEvent = confirm(`Удалить событие \"${elemTr.dataset.event}\"?`);
                if (!isRemoveEvent) return;
                let parameters = {
                    event: elemTr.dataset.event,
                    event_type: elemTr.dataset.type
                };
                if (elemTr.dataset.type == "online") {
                    parameters.handler = elemTr.dataset.handler;
                }
                let resDel = await this.apiClient.callMethod("event.unbind", parameters);
                if (resDel && resDel.count) {
                    elemTr.remove();
                }
            }
        })

        // Изменение типа события
        this.elemSelectTypeEvent.addEventListener("change", (e) => {
            this.setOfflineEvent(e.target.value);
        })

        // Кнопка содания события
        this.btnAddEvent.addEventListener("click", (e) => {
            this.addEvent();
        })
    }

    // Регистрирование события
    async addEvent() {
        let isOffline = 0;
        let parameters = {
            event: this.elemSelectNameEvent.value,
            event_type: this.elemSelectTypeEvent.value,
        };
        if (this.elemSelectTypeEvent.value == "online") {
            parameters.handler = this.elemInputHandlerEvent.value;
        } else {
            isOffline = 1
            parameters.auth_connector = this.elemInputSourceEvent.value;
        }
        console.log("Параметры создаваемого события: ", parameters);
        let resAddEvent = await this.apiClient.callMethod("event.bind", parameters);
        console.log("Результат создания события: ", resAddEvent);
        if (resAddEvent) {
            this.addRecordEventToTable(parameters.event, isOffline, parameters.handler, parameters.auth_connector);
        }
    }

    addRecordEventToTable(eventName, isOffline, eventHandler, eventConnector) {
        this.tBody = this.container.querySelector(".bx24_events__table_events tbody");
        let contentHTML = getRowEventHTML(eventName, isOffline, eventHandler, eventConnector);
        this.tBody.insertAdjacentHTML("beforeend", contentHTML);
    }

    setOfflineEvent(eventType) {
        if (eventType == "offline") {
            this.elemInputHandlerEvent.setAttribute("disabled", "");
            this.elemInputSourceEvent.removeAttribute("disabled");
        } else {
            this.elemInputHandlerEvent.removeAttribute("disabled");
            this.elemInputSourceEvent.setAttribute("disabled", "");
        }
    }

    async render() {
        const events = await this.apiClient.callMethod("event.get", {});
        const contentRegistredTableHTML = Templates.createTable(events);
        const contentHTML = Templates.createAppHTML(contentRegistredTableHTML, this.eventsList);
        this.container.innerHTML = contentHTML;
    }
}
