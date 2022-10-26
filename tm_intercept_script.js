// ==UserScript==
// @name         XHR Requests logger
// @namespace    http://tampermonkey.net/
// @version      0.2
// @description  None
// @author       None
// @match        https://myshows.me/*
// @icon         data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

(function(open) {
    XMLHttpRequest.prototype.open = function() {
        this.addEventListener("load", function() {
            if (!this.responseURL.includes('/rpc/')) {
                return;
            }

            // Request body
            // Response body
            // Status code
            // Endpoint
            // Method
            const request = {
                "host": document.location.host,
                "status_code": this.status,
                "endpoint": this.responseURL,
                "method": this.__sentry_xhr__.method,
                "request_body": this.__sentry_xhr__.body,
                "response_body": this.response
            };
            // console.log(this.responseURL, this.response, this.status);
            // console.log(this)
            // console.log(JSON.stringify(request))
            let xhr = new XMLHttpRequest();
            xhr.open("POST", "https://specify.domain/upload");

            xhr.setRequestHeader("Accept", "application/json");
            xhr.setRequestHeader("Content-Type", "application/json");

            xhr.send(JSON.stringify(request));

        }, false);
        open.apply(this, arguments);
    };
})(XMLHttpRequest.prototype.open);

})();