<template>
    <div>
      刷题
      <router-link to="/problems/1">点击进入第一题</router-link>
    </div>
</template>

<script>
  export default {
    data() {
      return {
        ret: []
      };
    },
    methods: {
      handleClick(tab, event) {
        console.log(tab, event);
      },
      getValue() {
        this.$axios.get("http://127.0.0.1:8000/api/v1/articles/").then(response => {
          this.ret = response.data
          console.log(response.data)
        })
      },
      postValue() {
        this.$axios.post("http://127.0.0.1:8000/api/v1/articles/").then(response => {
          this.ret = response.data
          console.log(response.data)
        })
      }
    },
	}
</script>