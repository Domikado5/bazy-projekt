import { createStore } from "vuex";

export default createStore({
  state: {
    token: null,
    url: 'http://localhost:8000'
  },
  getters: {
    getToken(state){
      return state.token
    },
    getUrl(state){
      return state.url
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
