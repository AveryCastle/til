import Vue from 'vue';

import store from './store';

import { mapState, mapActions } from 'vuex';

new Vue({
  el: '#app',
  store,
  computed: mapState([
    'tasks',
    'taskTitle',
  ]),
  methods: {
    ...mapActions([
      'fetchTasks',
      'addTask',
      'updateTaskTitle',
      'removeTask',
      'toggleTask',
    ]),
  },
  created() {
    this.fetchTasks();
  },
});