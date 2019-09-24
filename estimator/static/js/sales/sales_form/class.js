class RawMaterial{
    constructor(raw_material_pk, name, amount, measurement_unit, isBoughtInDollars, cost_dollar, cost_local, provider, providers_list) {
        this.raw_material_pk = raw_material_pk;
        this.name = name;
        this.amount = amount;
        this.measurement_unit = measurement_unit;
        this.isBoughtInDollars = isBoughtInDollars;
        this.cost_dollar = cost_dollar;
        this.cost_local = cost_local;
        this.provider = provider;
        this.providers_list = providers_list;
    }
    isAmountValid(){
        let num = Number.parseInt(this.amount);
        if(Number.isNaN(num)){
            return false;
        }
        if ( !(num >= 1)) {
            return false;
        }
        return true;
    }
    isDollarCostValid(){
        let num = Number.parseFloat(this.cost_dollar);
        if(Number.isNaN(num)){
            return false;
        }
        if (this.isBoughtInDollars && !(num > 0)) {
            return false;
        }
        return true;
    }
    isLocalCostValid(){
        let num = Number.parseFloat(this.cost_local);
        if(Number.isNaN(num)){
            return false;
        }
        if (!this.isBoughtInDollars && !(num > 0)) {
            return false;
        }
        return true;
    }
    isProviderValid(){
        self = this;
        let val = this.providers_list.find(function (el) {
            return el.pk === parseInt(self.provider);
        });
        if (val) {
            return true;
        }else{
            return false;
        }
    }

    isValid() {
        let isValid = true;
        if (! this.isAmountValid()) {
            isValid = false;
        }else if(! this.isDollarCostValid()) {
            isValid = false;
        }else if (! this.isLocalCostValid()) {
            isValid = false;
        } else if (!this.isProviderValid()) {
            isValid = false;
        }
        return isValid;
    }

    calculateLocalCost(){
        try {
            return this.cost_dollar * Number.parseFloat(app.dollar_price);
        } catch (error) {
            return this.cost_dollar * initial_dolar_price;
        }
    }

    calculateDolarCost(){
        try {
            return this.cost_local / Number.parseFloat(app.dollar_price);
        } catch (error) {
            return this.cost_local /  initial_dolar_price;
        }
    }
}