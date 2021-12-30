import { createStore } from "vuex";

export default createStore({
  state: {
    token: null,
  },
  getters: {
    getToken(state){
      return state.token
    }
  },
  mutations: {
    updateToken(state, payload){
      state.token = payload.token
    },
    resetToken(state){
      state.token = null
    }
  },
  actions: {},
  modules: {},
});
