<template>
  <div class="home">
    <h1>Fitapka</h1>
    <h4 class="text-start">Let's count some <span :class="{updateText: textUpdateActive}" class="green-text text-lighten-1" style="display: inline-block;">{{texts[index % 4]}}</span></h4>
  </div>
</template>

<script>

export default {
  name: "Home",
  components: {
    
  },
  data() {
    return {
      texts: ["proteins", "carbohydrates", "fats", "calories"],
      index: 0,
      timer: "",
      textUpdateActive: false,
    }
  },
  created(){
    this.timer = setInterval(this.incrementIndex, 1500);
  },
  methods: {
    incrementIndex(){
      this.textUpdateActive = false;
      setTimeout(() => {
        this.index += 1;
        this.textUpdateActive = true;
      }, 1000);
    },
    cancelTimer(){
      clearInterval(this.timer);
    },
  },
  beforeUnmount(){
    this.cancelTimer();
  },
};
</script>

<style lang="scss" scoped>
  .updateText{
    animation: textChange 0.5s linear 1 alternate;
  }

  @keyframes textChange {
    from{
      opacity: 0%;
    }
    50%{
      opacity: 50%;
    }
    to{
      opacity: 100%;
    }
  }

  h4 span{
    transform: width 5s;
  }
</style>