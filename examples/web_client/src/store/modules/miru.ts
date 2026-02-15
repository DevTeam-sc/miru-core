import { Module } from 'vuex';

interface MiruState {
  processes: Process[],
}

type Process = [number, string];

const miruModule: Module<MiruState, any> = {
  state: {
    processes: []
  },

  mutations: {
  }
};

export default miruModule;
