/** @odoo-module **/
import { Component, useState, onWillStart } from '@odoo/owl';
import { registry } from '@web/core/registry';
import { useService } from '@web/core/utils/hooks';
import { _t } from '@web/core/l10n/translation';

export async function resolvePromise(promise) {
    try {
        const result = await promise;
        return [result, null];
    } catch (error) {
        return [null, error];
    }
}

export const cityModel = 'res.city';
export const countryModel = 'res.country';
export const stateModel = 'res.country.state';
export const partnerModel = 'res.partner';

export class PostulationForm extends Component {
    static template = 'nena_partner_record.PostulationFormTemplate';

    setup() {
        this.state = useState({
            data: {},
            filterStates: [],
            filterCities: [],
            countries: [],
            files: {},
        });

        this.states = [];
        this.cities = [];

        this.orm = useService('orm');
        this.notification = useService('notification');
        this.attachmentUpload = useService('file_upload');

        onWillStart(async () => {
            try {
                console.log(this);
                const [data, error] = await resolvePromise(
                    Promise.all([
                        this.getCountries(),
                        this.getStates(),
                        this.getCities(),
                    ]),
                );

                if (error) {
                    this.notifyError(JSON.stringify(error));
                    return;
                }

                if (!data) {
                    this.notifyError(_t('Failed to load data'));
                    return;
                }

                const [countries, states, cities] = data;

                if (!countries || !states || !cities) {
                    this.notifyError(_t('Invalid data received'));
                    return;
                }

                this.state.countries = countries;
                this.states = states;
                this.cities = cities;

                if (countries.length > 0) {
                    this.state.data.company_country_id = countries[0].id;
                    this.updateStatesFilter();
                }
            } catch (error) {
                console.error('Error in onWillStart:', error);
                this.notifyError(_t('Error loading form data'));
            }
        });
    }

    _notify({ msg, title, type, options = {} }) {
        this.notification.add(msg, { title, type, ...options });
    }

    notifySuccess(msg) {
        this._notify({ msg, title: _t('Success'), type: 'success' });
    }

    notifyError(msg) {
        this._notify({ msg, title: _t('Error'), type: 'danger' });
    }

    _searchRead({
        model,
        domain = [],
        fields = ['id', 'name'],
        options = {},
        queue = false,
    }) {
        return this.orm.searchRead(model, domain, fields, options, queue);
    }

    _call({ model, method, ids = [], args = [] }) {
        return this.orm.call(model, method, [ids, ...args]);
    }

    async getCountries() {
        return this._searchRead({
            model: countryModel,
            fields: ['id', 'name', 'code'],
        });
    }

    async getStates() {
        return this._searchRead({
            model: stateModel,
            fields: ['id', 'name', 'country_id', 'code'],
        });
    }

    async getCities() {
        return this._searchRead({
            model: cityModel,
            fields: ['id', 'name', 'state_id', 'zipcode'],
        });
    }

    onChangeHandler(e) {
        this.state.data[e.target.name] = e.target.value;
    }

    onChangeCountryIdHandler(e) {
        this.onChangeHandler(e);
        this.updateStatesFilter();
    }

    onChangeStateIdHandler(e) {
        this.onChangeHandler(e);
        this.updateCitiesFilter();
    }

    onChangeCityIdHandler(e) {
        this.onChangeHandler(e);
        this.updateZipFromCity();
    }

    async onChangeFilesHandler(e) {
        const files = e.target.files;
        if (files.length === 0) return;

        const filesData = await Promise.all(
            Array.from(files).map((file) => this.readFileAsBase64(file)),
        );

        const attachmentsData = filesData.map((base64, index) => ({
            name: files[index].name,
            data: base64.split(',')[1],
        }));

        this.state.files[e.target.name] = attachmentsData;
    }

    async onSubmitHandler(e) {
        e.preventDefault();

        const partners = await this._call({
            method: 'js_create_customer',
            model: partnerModel,
            args: [this.state.data, this.state.files],
        });

        if (partners.length == 0) {
            this.notifyError(_t('Unknow Error'));
            return;
        }

        this.notifySuccess(_t('Success Create New Client'));
        setTimeout(() => e.target.reset(), 1000);
    }

    readFileAsBase64(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = () => resolve(reader.result);
            reader.onerror = (error) => reject(error);
            reader.readAsDataURL(file);
        });
    }

    updateZipFromCity() {
        const city = this.cities.find(
            (c) => c.id === +this.state.data.company_city_id,
        );

        if (!city) return;

        this.state.data.company_zip = city.zipcode;
    }

    updateCitiesFilter() {
        this.state.filterCities = this.cities.filter(
            (c) => c.state_id[0] === +this.state.data.company_state_id,
        );

        this.state.data.company_city_id = null;
        this.state.data.company_zip = null;

        if (this.state.filterCities.length === 0) return;

        this.state.data.company_city_id = this.state.filterCities[0].id;
        this.updateZipFromCity();
    }

    updateStatesFilter() {
        this.state.filterStates = this.states.filter(
            (s) => s.country_id[0] === +this.state.data.company_country_id,
        );

        this.state.data.company_state_id = null;
        this.state.data.company_city_id = null;
        this.state.data.company_zip = null;

        if (this.state.filterStates.length === 0) {
            this.state.filterStates = [];
            return;
        }

        this.state.data.company_state_id = this.state.filterStates[0].id;
        this.updateCitiesFilter();
    }
}

registry
    .category('public_components')
    .add('nena_partner_record.PostulationForm', PostulationForm);
