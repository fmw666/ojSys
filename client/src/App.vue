<template>
  <div id="app">
    <nav-bar></nav-bar>
    <transition :name="transitionName">
      <keep-alive include="placeOrder">
        <router-view/>
      </keep-alive>
    </transition>
  </div>
</template>

<script>
import NavBar from './components/navbar/NavBar.vue'
export default {
  name: 'App',
  data() {
    return {
      transitionName: 'fold-left'
    }
  },
  watch: {//使用watch 监听$router的变化
    $router(to, from) {
      //如果to索引大于from索引,判断为前进状态,反之则为后退状态
      if (to.meta.index > from.meta.index) {
        this.transitionName = 'fold-left';
      } else {
        this.transitionName = 'fold-right';
      }
    },
  },
  components: {
    NavBar
  },
}
</script>

<style>

body{
  margin: 0 !important;
  padding: 0;
  background-color: #C7EDCC;
}

.fold-left-enter-active {
  animation-name: fold-left-in;
  animation-duration: .7s;
}
.fold-left-leave-active {
  animation-name: fold-left-out;
  animation-duration: .7s;
}
@keyframes fold-left-in {
  0% {
    -webkit-transform: translate3d(100%, 0, 0);
    transform: translate3d(100%, 0, 0);
    /* visibility: visible; */
  }
  /*50% {
    transform: translate3d(50%, 0, 0);
  }*/
  100% {
    -webkit-transform: translate3d(0, 0, 0);
    transform: translate3d(0, 0, 0);
  }
}
@keyframes fold-left-out {
  0% {
    -webkit-transform: translate3d(0, 0, 0);
    transform: translate3d(0, 0, 0);
  }
  /*50% {
    transform: translate3d(-50%, 0 , 0);
  }*/
  100% {
    -webkit-transform: translate3d(-100%, 0, 0);
    transform: translate3d(-100%, 0, 0);
    /* visibility: hidden; */
  }
}
.fold-right-enter-active {
  animation-name: fold-right-in;
  animation-duration: .7s;
}
.fold-right-leave-active {
  animation-name: fold-right-out;
  animation-duration: .7s;
}
@keyframes fold-right-in{
  0% {
    width: 100%;
    -webkit-transform: translate3d(-100%, 0, 0);
    transform: translate3d(-100%, 0, 0);
    /* visibility: visible; */
  }
  /*50% {
    transform: translate3d(50%, 0, 0);
  }*/
  100% {
    width: 100%;
    -webkit-transform: translate3d(0, 0, 0);
    transform: translate3d(0, 0, 0);
  }
}
@keyframes fold-right-out  {
  0% {
    width: 100%;
    -webkit-transform: translate3d(0, 0, 0);
    transform: translate3d(0, 0, 0);
  }
  /*50% {
    transform: translate3d(-50%, 0 , 0);
  }*/
  100% {
    width: 100%;
    -webkit-transform: translate3d(100%, 0, 0);
    transform: translate3d(100%, 0, 0);
    /* visibility: hidden; */
  }
}

</style>