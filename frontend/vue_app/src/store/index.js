import { createStore } from "vuex";
import createPersistedState from 'vuex-persistedstate'

export default createStore({
  state: {
    token: null,
    url: 'http://localhost:8000',
    user: null,
  },
  plugins: [createPersistedState({
    storage: window.sessionStorage,
})],
  getters: {
    getToken(state){
      return state.token
    },
    getUrl(state){
      return state.url
    },
    getUser(state){
      return state.user
    },
  },
  mutations: {
    updateToken(state, payload){
      state.token = payload.token
      state.user = payload.user
    },
    resetToken(state){
      state.token = null
      state.user = null
      window.sessionStorage.clear()
    }
  },
  actions: {},
  modules: {},
});
