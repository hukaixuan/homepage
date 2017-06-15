<template>
    <div class="personal-center-wrap">
        <div class="personal-title">个人信息</div>
        <div class="form-wrap">
            <el-form ref="form" :model="form" label-width="80px">
                <el-form-item label="用户名">
                    <el-input v-model="form.username"></el-input>
                </el-form-item>
                <!-- <el-form-item label="博客说明">
                    <el-input v-model="form.individualitySignature"></el-input>
                </el-form-item> -->
                <el-form-item label="个人介绍">
                    <el-input type="textarea" class="textarea-height" v-model="form.describe"></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="onSubmit">保存修改</el-button>
                </el-form-item>
            </el-form>
        </div>
    </div>
</template>

<script>
import {getCookie} from '../utils/utils.js'
export default{
    data(){
        return{
            form: {
                username: '',
                describe: '',
            }
        }
    },
    mounted: function(){
        this.$http.get('http://127.0.0.1:5000/api/v1/users/1').then(
            // respone => this.form = respone.body[0],
            respone => this.form = respone.body,
            respone => this.$message.error('获取个人信息失败，请重试')
        )
    },

    methods: {
        onSubmit: function(){
            var options = {
                url: 'http://127.0.0.1:5000/api/v1/users/1',
                method: 'PUT',
                headers: 
                {
                    Authorization: 'Basic '+window.btoa(getCookie('token'))
                },
                body:
                {
                    username: this.form.username,
                    describe: this.form.describe
                }
            }
            this.$http(options).then(
                respone => this.$message('保存成功'),
                respone => this.$message.error('保存失败，请刷新页面重试')
            )
        }
    }
}
</script>

<style>
.personal-center-wrap {
    margin-left:90px;
    text-align: center;
}
.personal-title {
    font-size: 35px;
    color: #20a0ff;
    margin-top: 4rem;
    font-weight: bold;
}
.form-wrap {
    width: 500px;
    margin: 0 auto;
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    padding: 13px 16px;
}
.textarea-height > textarea {
    height: 150px;
}
</style>