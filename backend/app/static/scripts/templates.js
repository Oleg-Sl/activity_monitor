

export default class Templates {
    static createTable(eventsData) {
        let content = `
            <table class="table table-hover table-bordered caption-top bx24_events__table_events">
                <caption>Список установленных обработчиков событий</caption>
                <thead>
                    <tr>
                        <th scope="col">Событие</th>
                        <th scope="col">Тип события</th>
                        <th scope="col">URL обработчика</th>
                        <th scope="col">Коннектор</th>
                        <th scope="col"></th>
                    </tr>
                </thead>
                <tbody>
                    ${this.generateTbodyHTML(eventsData)}
                </tbody>
            </table>
        `;
        return content;
    }

    static generateTbodyHTML(eventsData) {
        let content = '';
        for (let eventData of eventsData) {
            content += this.getRowEventHTML(eventData.event, eventData.offline, eventData.handler, eventData.connector_id);
        }
        return content
    }
    
    static getRowEventHTML(name, isOffline, handler, connectorId) {
        let typeEventRus = isOffline ? "оффлайн" : "онлайн";
        let typeEventEng = isOffline ? "offline" : "online";
        return `
            <tr data-event="${name}" data-handler="${handler}" data-type="${typeEventEng}" data-connector="${connectorId}">
                <td scope="row">${name}</td>
                <td>${typeEventRus}</th>
                <td>${handler || ""}</td>
                <td>${connectorId || ""}</td>
                <td>
                    <div class="table-cell-settings bx24_events__table_events_remove_row">
                        <i class="bi bi-trash bx24_events__table_events_remove_row_i" title="Удалить"></i>
                    </div>
                </td>
            </tr>
        `;
    }

    static createAppHTML(contentRegistredTableHTML, eventsList) {
        let content = `
            <style type="text/css">
                .bx24_events__table_events_remove_row {
                    width: 100%;
                    height: 100%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }
                .bx24_events__table_events_remove_row i {
                    display: inline-block;
                    margin: 2px;
                    color: #797979;
                    font-size: 18px;
                    cursor: pointer;
                }
                .bx24_events__table_events_remove_row i::before {
                    font-weight: 700 !important;
                }
                .bx24_events__table_events_remove_row i:hover {
                    color: #000000;
                }
            </style>
            <div class="bx24_events__table_events_container">
                ${contentRegistredTableHTML}
            </div>
    
            <div class="bx24_events__registry_event_container">
                <h4>Регистрация событий</h4>
                <div class="border border-1 rounded p-3">
                    <div class="bx24_events__type_event">
                        <label for="registry_event__selectTypeEvent" class="form-label">Тип события</label>
                        <select class="form-select bx24_events__registry_event_select" aria-label="Default select example" id="registry_event__selectTypeEvent">
                            <option value="online" selected>Онлайн</option>
                            <option value="offline">Оффлайн</option>
                        </select>    
                    </div>
                    <div class="bx24_events__name_event">
                        <label for="name_event__selectTypeEvent" class="form-label">Название события</label>
                        <select class="form-select" aria-label="Default select example" id="name_event__selectTypeEvent">
                            ${getOptionsHTML(eventsList)}
                        </select>    
                    </div>
                    <div class="bx24_events__handler_event">
                        <label for="name_event__handlerEvent" class="form-label">URL обработчика</label>
                        <input class="form-control" type="text" placeholder="..." aria-label="input example" id="name_event__handlerEvent">
                    </div>
                    <div class="bx24_events__source_event">
                        <label for="name_event__sourceKey" class="form-label">Ключ источника</label>
                        <input class="form-control" type="text" placeholder="..." aria-label="input example" id="name_event__sourceKey">
                    </div>
                    <div class="d-grid gap-2 d-md-flex justify-content-md-end mt-2 bx24_events__add_event">
                        <button class="btn btn-primary me-md-2" type="button">Добавить</button>
                    </div>
                </div>
            </div>
        `;
        return content;
    }

    static getOptionsHTML(eventsList) {
        let contentHTML = '';
        for (let event of eventsList) {
            contentHTML += `<option value="${event}">${event}</option>`;
        }
        return contentHTML;
    }
}
