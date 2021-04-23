<template>
  <div>
    <div>
      <div class="" id="email_result">
        停两秒，返回 /account
        <div v-if="success" class="">恭喜您，邮箱验证成功！<br/><a href="/">返回主页</a></div>
        <div v-else class="">链接已失效，验证失败，请重新验证！<br/><a href="/">返回主页</a></div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "VerifyEmail",
  data() {
    return {
      success: true,
    }
  },
  methods: {

  },
  created: function(){
    this.$axios.get('http://127.0.0.1:8000/api/v1/emails/verification/'+ document.location.search)
       .then(response => {
           this.success = true;
       })
       .catch(error => {
           this.success = false;
       });
  }
}
</script>

<style scoped>

</style>