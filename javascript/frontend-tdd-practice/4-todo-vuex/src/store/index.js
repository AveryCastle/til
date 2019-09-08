import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

import Counter from '../utils/counter';

import actions from './actions';
import mutations from './mutations';

const state = {
  counter: Counter(),
  tasks: [],
  taskTitle: '',
};

export default new Vuex.Store({
  state,
  actions,
  mutations,
});