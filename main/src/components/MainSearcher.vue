<template>
    <v-container fill-height fluid class="pa-12 grey lighten-3">
        <v-row no-gutters class="fill-height" justify="center">
            <v-col cols="8">
                <v-card class="fill-height">
                    <v-card-text class="pb-0">
                        <div class="grey--text mb-2">Use the dropdown below to start searching for an address.</div>
                        <v-row no-gutters>
                            <v-autocomplete v-model="selectedAddress"
                                            label="Address"
                                            no-data-text="No available addresses"
                                            outlined
                                            :items="addresses"
                                            return-object
                                            :loading="loading"
                                            clearable
                                            @update:search-input="getAddresses($event)"
                            ></v-autocomplete>
                        </v-row>
                    </v-card-text>
                    <v-card-actions class="pt-0 px-4 pb-4">
                        <v-spacer></v-spacer>
                        <v-btn color="primary" :loading="loadingCheck" :disabled="selectedAddress === null" @click="check()">Check Availability</v-btn>
                    </v-card-actions>
                </v-card>
            </v-col>
        </v-row>
        <v-dialog width="500" v-model="hasError" persistent>
            <v-card>
                <v-card-title class="error">
                    <div class="white--text">Oops!</div>
                </v-card-title>
                <v-card-text>
                    <div class="font-weight-bold mt-3">It seems something went wrong on our side, please click try again or refresh this page.</div>
                </v-card-text>
                <v-card-actions class="pt-0 px-4 pb-4">
                    <v-spacer></v-spacer>
                    <v-btn color="error" @click="refresh()" :loading="loadingError">Try Again</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </v-container>
</template>

<script>
import debounce from 'debounce';

    export default {
        name: "MainSearcher",
        data: () => ({
            term: '',
            selectedAddress: null,
            addresses: [],
            loading: false,
            loadingCheck: false,
            loadingError: false,
            hasError: false
        }),
        methods: {
            checkStatus() {
                this.$http.get('https://nominatim.openstreetmap.org/status.php?format=json').then(
                    (resp) => {
                        if(resp.data.status !== 0) {
                            this.hasError = true;
                        }
                    },
                    (err) => {
                        this.hasError = true;
                        console.log(err);
                    }
                );
            },
            getAddresses: debounce(function (term) {
                if(term !== null) {
                this.term = term.split(' ').join('+');
                this.loading = true;
                // this.$http.get('https://nominatim.openstreetmap.org/search/?street=' + this.term + '&country=south+africa&format=json').then(
                this.$http.get('https://gis.telkom.co.za/locators/rest/services/Telkom_Composite/GeocodeServer/suggest?f=json&text='+this.term+'&maxSuggestions=10').then(
                    (resp) => {
                        this.addresses = resp.data.suggestions;
                        this.loading = false;
                    },
                    (err) => {
                        this.hasError = true;
                        console.log(err);
                        this.loading = false;
                    }
                );
                }
            }, 1000),
            check() {
                this.$http.post('http://localhost:5000/api/v1', JSON.stringify(this.selectedAddress)).then(
                    (resp) => {
                        console.log(resp);
                    },
                    (err) => {
                        console.log(err);
                        this.hasError = true;
                    }
                );
            },
            refresh() {
                this.loadingError = true;
                window.location.href = JSON.parse(JSON.stringify(window.location.href));
            }
        },
        mounted() {
            this.checkStatus();
        },
    }
</script>

<style scoped>

</style>