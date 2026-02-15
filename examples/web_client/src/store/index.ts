import Vue from 'vue';
import Vuex from 'vuex';

import miru from './modules/miru';
import miruBus from './plugins/miru';

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    miru
  },
  plugins: [
    miruBus()
  ]
});
