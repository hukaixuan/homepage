<template>
    <div class="personal-center-wrap">
        <div class="personal-title">登录</div>
        <div class="form-wrap">
            <el-form ref="form" :model="credentials" label-width="80px">
                <el-form-item label="用户名">
                    <el-input v-model="credentials.username"></el-input>
                </el-form-item>
                <!-- <el-form-item label="博客说明">
                    <el-input v-model="form.individualitySignature"></el-input>
                </el-form-item> -->
                <el-form-item label="密码">
                    <el-input type="password" v-model="credentials.password"></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="submit">登录</el-button>
                </el-form-item>
            </el-form>
        </div>
    </div>
  </template>

  <script>
  // import auth from '../auth'
  import {setCookie} from '../utils/utils.js'
  import { Message } from 'element-ui';
  export default {
    data() {
      return {
        // We need to initialize the component with any
        // properties that will be used in it
        credentials: {
          username: '',
          password: ''
        },
        error: ''
      }
    },
    methods: {
      submit() {
        var encodedData = window.btoa(this.credentials.username+':'+this.credentials.password)
        var options = {
            url: 'http://127.0.0.1:5000/auth/request-token',
            method: 'POST',
            headers: 
            {
                Authorization: 'Basic '+encodedData
            }
        }
        this.$http(options).then(
            response => {
                setCookie('token', response.data.token, 1)  // 设置cookie的过期时间为一天
                this.$router.push('/articleList')
                Message.success('登录成功！')
            },
            response => {
                Message.error('用户名或密码错误！')
            }
        )
      }
    }

  }
  </script>