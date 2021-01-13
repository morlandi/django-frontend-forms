
////////////////////////////////////////////////////////////////////////////////
// base Dialog

class Dialog {

    /**
     * Constructor
     *
     * @param {object} options - check "this.options" defaults for a full list of available options
     */

    constructor(options={}) {

        self = this;

        // Default options
        self.options = {
            dialog_selector: '#dialog_generic',
            open_event: null,
            html: '',
            url: '',
            width: null,
            min_width: null,
            max_width: null,
            height: null,
            min_height: null,
            max_height: null,
            button_save_label: gettext('Save'),
            button_save_initially_hidden: false,
            button_close_label: gettext('Cancel'),
            title: '',
            footer_text: '',
            enable_trace: false,
            callback: null,
            autofocus_first_visible_input: true
        };

        // Override with user-supplied custom options
        if (options) {
            Object.assign(self.options, options);
        }

        self.element = $(self.options.dialog_selector);
        if (self.element.length <= 0) {
            var message = 'ERROR: dialog "' + self.options.dialog_selector + '" not found';
            console.log(message);
            FrontendForms.display_server_error(message);
        }

        self._notify("created", {options: self.options});
    }

    /**
     * Fire a custom "Dialog" event.
     *
     * Sample usage in this class:
     *    this._notify("created", ['foo', 'bar']);
     *
     * Sample usage client-side:
     *
     *  $('#dialog_generic').on('created.dialog', function(event, arg1, arg2) {
     *      var target = $(event.target);
     *      console.log('Dialog created: target=%o, arg1=%o, arg2=%o', target, arg1, arg2);
     *  });
     */

    // _notify(event_name, event_info=[]) {
    //     var self = this;
    //     if (self.options.enable_trace) {
    //         console.log('[Dialog] ' + event_name + ' %o', event_info);
    //     }
    //     self.element.trigger(event_name + ".dialog", [self].concat(event_info));
    // }

    _notify(event_name, params={}) {
        var self = this;
        if (self.options.enable_trace) {
            console.log('[Dialog ' + event_name + '] dialog: %o; params:%o', self, params);
        }
        if (self.options.callback) {
            self.options.callback(event_name, self, params);
        }
    }

    /**
     * Getters and setters
     */

    //get element() { return this._element; }
    //get options() { return this._options; }

    /**
     * Close (hide) the dialog
     */

    close() {
        var self = this;

        self.element.find('.close').off();
        //$(window).off();
        self.element.hide();

        // Restore normal page scrolling in case the recently opened modal
        // had disable it to scroll it's own contents instead
        $('body').css('overflow', 'auto');

        self._notify('closed');
    }

    _initialize(open_event) {
        var self = this;

        self.options.open_event = open_event;

        var content = self.element.find('.dialog-content');
        var header = content.find('.dialog-header');
        var body = content.find('.dialog-body');
        var footer = content.find('.dialog-footer');

        if (self.options.width) { content.css('width', self.options.width); }
        if (self.options.min_width) { content.css('min-width', self.options.min_width); }
        if (self.options.max_width) { content.css('max-width', self.options.max_width); }
        if (self.options.height) { body.css('height', self.options.height); }
        if (self.options.min_height) { body.css('min-height', self.options.min_height); }
        if (self.options.max_height) { body.css('max-height', self.options.max_height); }

        header.find('.title').html('&nbsp;' + self.options.title);
        footer.find('.text').html('&nbsp;' + self.options.footer_text);

        var btn_save = footer.find('.btn-save');
        if (self.options.button_save_label === null) {
            btn_save.hide();
        }
        else {
            btn_save.val(self.options.button_save_label);
            if (self.options.button_save_initially_hidden) {
                // Visualization postponed after form rendering
                btn_save.hide();
            }
        }
        var btn_close = footer.find('.btn-close');
        if (self.options.button_close_label === null) {
            btn_close.hide();
        }
        else {
            btn_close.val(self.options.button_close_label);
        }

        self._notify('initialized');
    }

    /**
     * Show the dialog
     */

    show() {
        var self = this;
        self.element.show();
        self._notify('shown');
    }

    _load() {

        var self = this;
        var header = self.element.find('.dialog-header');

        self._notify('loading', {url: self.options.url});
        header.addClass('loading');
        var promise = $.ajax({
            type: 'GET',
            url: self.options.url,
            cache: false,
            crossDomain: true,
            headers: {
                // make sure request.is_ajax() return True on the server
                'X-Requested-With': 'XMLHttpRequest'
            }
        }).done(function(data, textStatus, jqXHR) {
            self.element.find('.dialog-body').html(data);
            self._notify('loaded', {url: self.options.url, data: data});
        }).fail(function(jqXHR, textStatus, errorThrown) {
            self._notify('loading_failed', {jqXHR: jqXHR, textStatus: textStatus, errorThrown: errorThrown});
            console.log('ERROR: errorThrown=%o, textStatus=%o, jqXHR=%o', errorThrown, textStatus, jqXHR);
            FrontendForms.display_server_error(errorThrown);
        }).always(function() {
            header.removeClass('loading');
        });

        return promise;
    }

    /**
     * Open the dialog
     *
     * 1. dialog body will be immediately loaded with static content "options.html"
     * 2. then the dialog is shown (unless the "show" parameter is false)
     * 3. finally, dynamic content will be loaded from remote address "options.url" (if supplied)
     * 4. if successfull, a 'loaded.dialog' event is fired; you can use it to perform any action required after loading
     */

    open(event=null, show=true) {

        var self = this;
        self._initialize(event);

        // When the user clicks on any '.btn-close' element, close the modal
        self.element.find('.dialog-header .close').off().on('click', function() {
            self.close();
        });

        // Handle Close botton in the footer, if any
        var btn_close = self.element.find('.dialog-footer .btn-close');
        if (btn_close.length) {
            btn_close.off().on('click', function(event) {
                self.close();
            });
        }

        /*
        // When the user clicks anywhere outside of the modal, close it
        $(window).off().on('click', function(event) {
            //if (event.target.id == modal.attr('id')) {
            if (event.target == self.element.get(0)) {
                self.close();
            }
        });
        */

        if (self.element.hasClass('draggable')) {
            self.element.find('.dialog-content').draggable({
                handle: '.dialog-header'
            });
        }

        // Load static content
        self.element.find('.dialog-body').html(self.options.html);
        self._notify('open');

        // Show the dialog
        if (show) {
            self.show();
        }

        // Load remote content
        if (self.options.url) {
            self._load().done(function(data, textStatus, jqXHR) {
                var form = self.element.find('.dialog-content .dialog-body form');
                if (form.length == 1) {
                    // Manage form
                    self._form_ajax_submit();
                }
            });
        }
    }

    _form_ajax_submit() {
        var self = this;

        var content = self.element.find('.dialog-content');
        var header = content.find('.dialog-header');
        var body = content.find('.dialog-body');
        var footer = content.find('.dialog-footer');
        var form = content.find('.dialog-body form');

        // use footer save button, if available
        var btn_save = footer.find('.btn-save');
        if (self.options.button_save_label !== null && btn_save) {
            form.find('.form-submit-row').hide();
            btn_save.off().on('click', function(event) {
                form.submit();
            });
            btn_save.show();
        }

        // Give focus to first visible form field
        if (self.options.autofocus_first_visible_input) {
            form.find('input:visible').first().focus().select();
        }

        // bind to the form’s submit event
        form.on('submit', function(event) {

            // prevent the form from performing its default submit action
            event.preventDefault();
            header.addClass('loading');

            // serialize the form’s content and send via an AJAX call
            // using the form’s defined method and action
            var url = form.attr('action') || self.options.url;
            var method = form.attr('method') || 'post';
            var data = form.serialize();

            self._notify('submitting', {method: method, url: url, data:data});
            $.ajax({
                type: method,
                url: url,
                data: data,
                cache: false,
                crossDomain: true,
                headers: {
                    // make sure request.is_ajax() return True on the server
                    'X-Requested-With': 'XMLHttpRequest'
                }
            }).done(function(xhr, textStatus, jqXHR) {

                // update the modal body with the new form
                body.html(xhr);

                // Does the response contain a form ?
                var form = self.element.find('.dialog-content .dialog-body form');
                if (form.length > 0) {
                    // If the server sends back a successful response,
                    // we need to further check the HTML received

                    // If xhr contains any field errors,
                    // the form did not validate successfully,
                    // so we keep it open for further editing
                    //if ($(xhr).find('.has-error').length > 0) {
                    if ($(xhr).find('.has-error').length > 0 || $(xhr).find('.errorlist').length > 0) {
                        self._notify('loaded', {url: url});
                        self._form_ajax_submit();
                    } else {
                        // otherwise, we've done and can close the modal
                        self._notify('submitted', {method: method, url: url, data: data});
                        self.close();
                    }
                }
                // If not, assume we received a feedback for the user after successfull submission, so:
                // - keep the dialog open
                // - hide the save button
                else {
                    // We also notify the user about successful submission
                    self._notify('submitted', {method: method, url: url, data: data});
                    btn_save.hide();
                }

            }).fail(function(jqXHR, textStatus, errorThrown) {
                console.error('ERROR: errorThrown=%o, textStatus=%o, jqXHR=%o', errorThrown, textStatus, jqXHR);
                console.error(jqXHR.responseText);
                FrontendForms.display_server_error(errorThrown);
            }).always(function() {
                header.removeClass('loading');
            });
        });
    }

}

////////////////////////////////////////////////////////////////////////////////
// Helpers

window.FrontendForms = (function() {

    function display_server_error(errorDetails) {

        // Try with SweetAlert2
        try {
            swal.fire({
                confirmButtonClass: 'btn btn-lg btn-primary',
                cancelButtonClass: 'btn btn-lg btn-default',
                buttonsStyling: false,
                reverseButtons: true,
                title: gettext('ERROR'),
                text: errorDetails,
                type: 'error',
                icon: 'error',
                confirmButtonClass: 'btn btn-lg btn-danger',
                confirmButtonText: gettext('Close')
            });
        }
        // failing that, we fallback to a simple alert
        catch (err) {
            alert(errorDetails);
        }
    }

    /*
     * Routing
     */

    function redirect(url, show_layer=false) {
        // see: http://stackoverflow.com/questions/503093/how-can-i-make-a-redirect-page-in-jquery-javascript
        // similar behavior as an HTTP redirect
        console.log('redirect(): ' + url);
        if (show_layer) {
            overlay_show('body');
        }
        window.location.replace(url);
    }

    function gotourl(url, show_layer=false) {
        // see: http://stackoverflow.com/questions/503093/how-can-i-make-a-redirect-page-in-jquery-javascript
        // similar behavior as clicking on a link
        console.log('gotourl(): ' + url);
        if (show_layer) {
            overlay_show('body');
        }
        window.location.href = url;
    }

    function reload_page(show_layer=false) {
        if (show_layer) {
            overlay_show('body');
        }
        window.location.reload(true);
    }


    /*
     *  Overlay
     *
     *  Requires: gasparesganga-jquery-loading-overlay
     */

    function overlay_show(element) {
        $(element).LoadingOverlay(
            'show', {
                //background: 'rgba(0, 167, 140, 0.2)',
                background: 'rgba(0, 0, 0, 0.3)',
                image: '',
                fontawesome: 'fa fa-cog fa-spin'
            }
        );
    }

    function overlay_hide(element) {
        $(element).LoadingOverlay('hide');
    }

    function hide_mouse_cursor() {
        // https://stackoverflow.com/questions/9681080/changing-cursor-to-waiting-in-javascript-jquery#25207986
        //$('body').css('cursor', 'none');
        //$('body').addClass('waiting');
        $("body").css("cursor", "none");
    }


    /*
     *  "Object" helpers
     */

    // Speed up calls to hasOwnProperty
    var hasOwnProperty = Object.prototype.hasOwnProperty;

    function logObject(element, obj) {
        var html = '<table class="datatable">';
        for (key in obj) {
            if (key[0] == '*') {
                html += sprintf('<tr><td colspan="2" style="height: 100px;">%s</td></tr>', obj[key]);
            }
            else {
                html += sprintf('<tr><td style="width: 100px;">%s</td><td>%s</td></tr>', key, dumpObject(obj[key], 1, 0));
            }
        }
        html += '</table>';
        element.html(html);
    }

    function dumpObject(obj, max_depth, depth) {
        if (depth >= max_depth) {
            if (typeof obj == "object") {
                return '{...}';
            }
            else {
                return '...';
            }
        }
        var text = '';
        if (typeof obj == "object") {
            text = "{";
            var property = '';
            for (property in obj) {
                var child = obj[property];
                if (typeof child == "object") {
                    text += '"' + property + '": ' + dumpObject(child, max_depth - 1, depth + 1) + '; ';
                }
                else {
                    text += '"' + property + '": ' + child + ', ';
                }
            }
            text += "}";
        }
        else {
            text = obj;
        }
        return text;
    }

    // http://stackoverflow.com/questions/4994201/is-object-empty
    function isEmptyObject(obj) {

        // null and undefined are "empty"
        if (obj == null) return true;

        // Assume if it has a length property with a non-zero value
        // that that property is correct.
        if (obj.length > 0)    return false;
        if (obj.length === 0)  return true;

        // If it isn't an object at this point
        // it is empty, but it can't be anything *but* empty
        // Is it empty?  Depends on your application.
        if (typeof obj !== "object") return true;

        // Otherwise, does it have any properties of its own?
        // Note that this doesn't handle
        // toString and valueOf enumeration bugs in IE < 9
        for (var key in obj) {
            if (hasOwnProperty.call(obj, key)) return false;
        }

        return true;
    }

    // https://stackoverflow.com/questions/122102/what-is-the-most-efficient-way-to-deep-clone-an-object-in-javascript#122190
    function cloneObject(obj) {
        if (obj === null || typeof (obj) !== 'object' || 'isActiveClone' in obj)
            return obj;

        if (obj instanceof Date)
            var temp = new obj.constructor(); //or new Date(obj);
        else
            var temp = obj.constructor();

        for (var key in obj) {
            if (Object.prototype.hasOwnProperty.call(obj, key)) {
                obj['isActiveClone'] = null;
                temp[key] = cloneObject(obj[key]);
                delete obj['isActiveClone'];
            }
        }
        return temp;
    }

    // Find an Object by attribute in an Array
    // http://stackoverflow.com/questions/5579678/jquery-how-to-find-an-object-by-attribute-in-an-array#19154349
    function lookup(array, prop, value) {
        for (var i = 0, len = array.length; i < len; i++)
            if (array[i] && array[i][prop] === value) return array[i];
        return null;
    }


    // Adapts canvas size to desired size;
    function adjust_canvas_size(id) {
    /*
        Usage:

            <canvas id="{{client.id}}-chart1" style="width: 100%; height:200px;">
            </canvas>

            ...

            <script type="text/javascript">
                adjust_canvas_size("{{client.id}}-chart1");
            < /script>

        Adapted from:
        https://stackoverflow.com/questions/18679414/how-put-percentage-width-into-html-canvas-no-css#18680851
    */

        /// get computed style for canvas
        var canvas = document.getElementById(id);
        var cs = getComputedStyle(canvas);

        /// these will return dimensions in *pixel* regardless of what
        /// you originally specified for image:
        var width = parseInt(cs.getPropertyValue('width'), 10);
        var height = parseInt(cs.getPropertyValue('height'), 10);

        // /// now use this as width and height for your canvas element:
        // var canvas = document.getElementById(id);

        canvas.width = width;
        canvas.height = height;
    }


    function getCookie(name) {
        var value = '; ' + document.cookie,
            parts = value.split('; ' + name + '=');
        if (parts.length == 2) return parts.pop().split(';').shift();
    }


    /**
     * Invoke remote action upon user confirmation.
     *
     * Display a dialog to ask for user confirmation, then invoke remote action;
     * after successfull execution, call supplied callback with server result.
     *
     * @param {string}              url                 Server action to be invoked.
     * @param {object}              options             Display options.
     * @param {afterDoneCallback}   [function]          Callback to be invoked after successfull execution.
     * @param {object}              data (optional)     If supplied, call server action via POST (instead of get) passing by data
     *
     * @return {none}
     *
     *  Requires: sweetalert2
     *
     */

    function confirmRemoteAction(url, options, afterDoneCallback, data=null) {

        var _options = {
            confirmButtonClass: 'btn-success',
            cancelButtonClass: 'btn-default',
            buttonsStyling: false,
            reverseButtons: true,
            title: 'Are you sure ?',
            text: '',
            type: 'warning',
            showCancelButton: true,
            cancelButtonText: 'Cancel',
            confirmButtonText: 'Confirm'
        };
        Object.assign(_options, options);

        _options.confirmButtonClass += ' btn btn-lg';
        _options.cancelButtonClass += ' btn btn-lg';

        swal.fire(
        // {
        //     confirmButtonClass: 'btn btn-lg ' + _options.confirmButtonClass,
        //     cancelButtonClass: 'btn btn-lg ' + _options.cancelButtonClass,
        //     buttonsStyling: _options.buttonsStyling,
        //     reverseButtons: _options.reverseButtons,
        //     title: _options.title,
        //     text: _options.text,
        //     type: _options.type,
        //     showCancelButton: _options.showCancelButton,
        //     cancelButtonText: _options.cancelButtonText,
        //     confirmButtonText: _options.confirmButtonText,
        // }
            _options
        ).then((result) => {
            if (result.value) {
                // User selected "Yes", so proceed with remote call
                var promise = null;
                if (data === null) {
                    promise = $.ajax({
                        type: 'GET',
                        url: url
                    });
                }
                else {
                    promise = $.ajax({
                        type: 'POST',
                        url: url,
                        data: data,
                        cache: false,
                        crossDomain: true,
                        dataType: 'json',
                        headers: {
                            'X-CSRFToken': getCookie('csrftoken'),
                            'X-Requested-With': 'XMLHttpRequest'  // make sure request.is_ajax() return True on the server
                        }
                    });
                }
                promise.done(function(data) {
                    if (afterDoneCallback) {
                        afterDoneCallback(data);
                    }
                }).fail(function(jqXHR, textStatus, errorThrown) {
                    console.log('ERROR: ' + jqXHR.responseText);
                    display_server_error(errorThrown);
                });
            } else if (result.dismiss === swal.DismissReason.cancel) {
                // Read more about handling dismissals
            }
        });
    }


    // http://stackoverflow.com/questions/16086162/handle-file-download-from-ajax-post#23797348
    function downloadFromAjaxPost(url, params, headers, callback) {

        // NOTE:
        // jQuery ajax is not able to handle binary responses properly (can't set responseType),
        // so it's better to use a plain XMLHttpRequest call.

        /*
        $.ajax({
            url: url,
            type: 'post',
            //mimeType: 'application/pdf',
            dataType: 'text',
            //headers: {"Content-Type": "application/pdf"},
            data: params
        }).done(function(response, status, xhr) {
            console.log('response length: %o', response.length);
            console.log('status: %o', status);
            console.log('xhr: %o', xhr);

            var filename = "";
            var disposition = xhr.getResponseHeader('Content-Disposition');
            if (disposition && disposition.indexOf('attachment') !== -1) {
                var filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
                var matches = filenameRegex.exec(disposition);
                if (matches != null && matches[1]) filename = matches[1].replace(/['"]/g, '');
            }
            var type = xhr.getResponseHeader('Content-Type');

            var blob = new Blob([response], { type: type });

            console.log('disposition: %o', disposition);
            console.log('filename: %o', filename);
            console.log('type: %o', type);
            console.log('blob: %o', blob);

            if (typeof window.navigator.msSaveBlob !== 'undefined') {
                // IE workaround for "HTML7007: One or more blob URLs were revoked by closing the blob for which they were created. These URLs will no longer resolve as the data backing the URL has been freed."
                window.navigator.msSaveBlob(blob, filename);
            } else {
                var URL = window.URL || window.webkitURL;
                var downloadUrl = URL.createObjectURL(blob);

                if (filename) {
                    // use HTML5 a[download] attribute to specify filename
                    var a = document.createElement("a");
                    // safari doesn't support this yet
                    if (typeof a.download === 'undefined') {
                        window.location = downloadUrl;
                    } else {
                        a.href = downloadUrl;
                        a.download = filename;
                        document.body.appendChild(a);
                        a.click();
                    }
                } else {
                    window.location = downloadUrl;
                }

                setTimeout(function() { URL.revokeObjectURL(downloadUrl); }, 100); // cleanup
            }
        }).fail(function(jqXHR, textStatus, errorThrown) {
            console.log('jqXHR: %o', jqXHR);
            console.log('textStatus: %o', textStatus);
            console.log('errorThrown: %o', errorThrown);
            alert('Error: ' + textStatus);
        });
        */

        var xhr = new XMLHttpRequest();
        xhr.open('POST', url, true);
        xhr.responseType = 'arraybuffer';
        xhr.onload = function() {
            if (this.status === 200) {
                var filename = "";
                var disposition = xhr.getResponseHeader('Content-Disposition');
                if (disposition && disposition.indexOf('attachment') !== -1) {
                    var filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
                    var matches = filenameRegex.exec(disposition);
                    if (matches != null && matches[1]) filename = matches[1].replace(/['"]/g, '');
                }
                var type = xhr.getResponseHeader('Content-Type');

                var blob = new Blob([this.response], { type: type });
                if (typeof window.navigator.msSaveBlob !== 'undefined') {
                    // IE workaround for "HTML7007: One or more blob URLs were revoked by closing the blob for which they were created. These URLs will no longer resolve as the data backing the URL has been freed."
                    window.navigator.msSaveBlob(blob, filename);
                } else {
                    var URL = window.URL || window.webkitURL;
                    var downloadUrl = URL.createObjectURL(blob);

                    if (filename) {
                        // use HTML5 a[download] attribute to specify filename
                        var a = document.createElement("a");
                        // safari doesn't support this yet
                        if (typeof a.download === 'undefined') {
                            window.location = downloadUrl;
                        } else {
                            a.href = downloadUrl;
                            a.download = filename;
                            document.body.appendChild(a);
                            a.click();
                        }
                    } else {
                        window.location = downloadUrl;
                        // if (target !== undefined) {
                        //     window.open(downloadUrl, target);
                        // }
                        // else {
                        //     window.location.href = downloadUrl;
                        // }
                    }

                    setTimeout(function() { URL.revokeObjectURL(downloadUrl); }, 100); // cleanup
                }
            }
            if (callback) {
                callback();
            }
        };
        xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
        $.each(headers, function(key, value) {
            xhr.setRequestHeader(key, value);
        });

        xhr.send($.param(params));
    }


    //
    // Adapted from:
    // https://github.com/Gozala/querystring
    //
    // If obj.hasOwnProperty has been overridden, then calling
    // obj.hasOwnProperty(prop) will break.
    // See: https://github.com/joyent/node/issues/1707
    function hasOwnProperty2(obj, prop) {
        return Object.prototype.hasOwnProperty.call(obj, prop);
    }

    function querystring_parse(qs, sep, eq, options) {
        sep = sep || '&';
        eq = eq || '=';
        var obj = {};

        if (typeof qs !== 'string' || qs.length === 0) {
            return obj;
        }

        var regexp = /\+/g;
        qs = qs.split(sep);

        var maxKeys = 1000;
        if (options && typeof options.maxKeys === 'number') {
            maxKeys = options.maxKeys;
        }

        var len = qs.length;
        // maxKeys <= 0 means that we should not limit keys count
        if (maxKeys > 0 && len > maxKeys) {
            len = maxKeys;
        }

        for (var i = 0; i < len; ++i) {
            var x = qs[i].replace(regexp, '%20'),
                idx = x.indexOf(eq),
                kstr, vstr, k, v;

            if (idx >= 0) {
                kstr = x.substr(0, idx);
                vstr = x.substr(idx + 1);
            } else {
                kstr = x;
                vstr = '';
            }

            k = decodeURIComponent(kstr);
            v = decodeURIComponent(vstr);

            if (!hasOwnProperty2(obj, k)) {
                obj[k] = v;
            } else if (Array.isArray(obj[k])) {
                obj[k].push(v);
            } else {
                obj[k] = [obj[k], v];
            }
        }

        return obj;
    }

    function set_datepicker_defaults(language_code) {

        // https://stackoverflow.com/questions/494958/how-do-i-localize-the-jquery-ui-datepicker#30937754
        $.datepicker.regional['it-it'] = {
            closeText: 'Chiudi', // set a close button text
            currentText: 'Oggi', // set today text
            monthNames: ['Gennaio','Febbraio','Marzo','Aprile','Maggio','Giugno',   'Luglio','Agosto','Settembre','Ottobre','Novembre','Dicembre'], // set month names
            monthNamesShort: ['Gen','Feb','Mar','Apr','Mag','Giu','Lug','Ago','Set','Ott','Nov','Dic'], // set short month names
            dayNames: ['Domenica','Luned&#236','Marted&#236','Mercoled&#236','Gioved&#236','Venerd&#236','Sabato'], // set days names
            dayNamesShort: ['Dom','Lun','Mar','Mer','Gio','Ven','Sab'], // set short day names
            dayNamesMin: ['Dom','Lun','Mar','Mer','Gio','Ven','Sab'], // set short day names
            //dayNamesMin: ['Do','Lu','Ma','Me','Gi','Ve','Sa'], // set more short days names
            dateFormat: 'dd/mm/yy' // set format date
        };

        $.datepicker.common = {
            inline: true,
            // nextText: '&rarr;',
            // prevText: '&larr;',
            nextText: '<i class="fa fa-arrow-right"></i>',
            prevText: '<i class="fa fa-arrow-left"></i>',
            showOtherMonths: true,
            // dateFormat: 'dd MM yy',
            // dayNamesMin: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
            //showOn: "button",
            showOn: "both",
            // buttonImage: "img/calendar-blue.png",
            // buttonImageOnly: true,
            buttonText: "<i class='fa fa-calendar'></i>",
        };

        $.datepicker.setDefaults($.datepicker.common);
        if (language_code) {
            $.datepicker.setDefaults($.datepicker.regional[language_code]);
        }
    }

    /* Apply multiSelect with search capabilities to a '<select ... multiple="">' element */

    /*
     * TODO: add support for SELECT ALL
     *
     * see: https://stackoverflow.com/questions/39007371/jquery-multiselect-select-all-and-with-filtered-search
     */

    function apply_multiselect(elements) {
        $(elements).multiSelect({
            selectableHeader: "<input type='text' class='form-control search-input' autocomplete='off' placeholder='cerca ...'>",
            selectionHeader: "<input type='text' class='form-control search-input' autocomplete='off' placeholder='cerca ...'>",
            afterInit: function(ms) {
                var that = this,
                    $selectableSearch = that.$selectableUl.prev(),
                    $selectionSearch = that.$selectionUl.prev(),
                    selectableSearchString = '#' + that.$container.attr('id') + ' .ms-elem-selectable:not(.ms-selected)',
                    selectionSearchString = '#' + that.$container.attr('id') + ' .ms-elem-selection.ms-selected';

                that.qs1 = $selectableSearch.quicksearch(selectableSearchString)
                    .on('keydown', function(e) {
                        if (e.which === 40) {
                            that.$selectableUl.focus();
                            return false;
                        }
                    });

                that.qs2 = $selectionSearch.quicksearch(selectionSearchString)
                    .on('keydown', function(e) {
                        if (e.which == 40) {
                            that.$selectionUl.focus();
                            return false;
                        }
                    });
            },
            afterSelect: function() {
                this.qs1.cache();
                this.qs2.cache();
            },
            afterDeselect: function() {
                this.qs1.cache();
                this.qs2.cache();
            }
        });
    }

    return {
        display_server_error: display_server_error,
        redirect: redirect,
        gotourl: gotourl,
        reload_page: reload_page,
        overlay_show: overlay_show,
        overlay_hide: overlay_hide,
        hide_mouse_cursor: hide_mouse_cursor,
        logObject: logObject,
        dumpObject: dumpObject,
        isEmptyObject: isEmptyObject,
        cloneObject: cloneObject,
        lookup: lookup,
        adjust_canvas_size: adjust_canvas_size,
        getCookie: getCookie,
        confirmRemoteAction: confirmRemoteAction,
        downloadFromAjaxPost: downloadFromAjaxPost,
        querystring_parse: querystring_parse,
        set_datepicker_defaults: set_datepicker_defaults,
        apply_multiselect: apply_multiselect
    };

})();

