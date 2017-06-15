<template>
    <div>
        <el-row :gutter="0"  v-scroll="loadMore">
            <el-col :xs="22" :sm="22" :md="20" :lg="20" :push="1">
                <div class="grid-content bg-purple">
                    <el-tabs>
                        <el-tab-pane label="最新文章">
                            <el-row :gutter="20">
                                <!-- <el-col :xs="24" :sm="12" :md="12" :lg="12" v-for="item in articleList" :key="item._id"> -->
                                <el-col :xs="24" :sm="12" :md="12" :lg="12" v-for="item in articleList">
                                    <el-card class="box-card articles-box">
                                        <div class="post-title" @click="articlesDetailsFn(item.id)">
                                            {{item.title}}
                                        </div>
                                        <div class="post-time">
                                            {{new Date(item.post_time).format('yyyy-MM-dd hh:mm:ss')}}
                                            <span class="post-label">🚩 {{item.label_name}}</span>
                                        </div>
                                        <div class="post-abstract" v-compiledMarkdown>
                                            {{item.content}}。
                                        </div>
                                        <!-- {{item.title}} -->
                                    </el-card>
                                </el-col>
                            </el-row>
                        </el-tab-pane>
                    </el-tabs>
                </div>
            </el-col>
        </el-row>
    </div>
</template>
<script>
import marked from 'marked';
import highlight from 'highlight.js'
import '../assets/atom-one-light.css'
import {dateFormat} from '../utils/utils.js'
export default {
    name: 'latestArticles',
    data() {
        return {
            articleList: [],
            // total: 1000,
            // current_page: 1,
            page: 1,
            scrollDisable: false
        }
    },
    mounted() {
        dateFormat()
        marked.setOptions({
            renderer: new marked.Renderer(),
            gfm: true,
            tables: true,
            breaks: false,
            pedantic: false,
            sanitize: false,
            smartLists: true,
            smartypants: false,
            highlight: function(code) {
                return highlight.highlightAuto(code).value;
            }
        })
        this.$http.get('/api/v1/posts?page='+this.page+'per_page=10&expand=1').then(
                res => {
                    console.log(res)
                    this.articleList = res.data.posts
                    console.log('=============')
                    this.page += 1
                }
            )
    },
    methods: {
        articlesDetailsFn: function(id) {
            this.$router.push({
                name: 'articlesDetails',
                params: {
                    id: id
                }
            })
        },
        loadMore() {
            console.log('ddddd')
            if (!this.scrollDisable) {
                // 一开始加载，就将 scrollDisable 设置为 true，即使触发了多次 loadMore，都只会执行一次下面的代码
                this.scrollDisable = true
                this.$http.get('/api/v1/posts?page='+this.page+'per_page=10&expand=1').then(
                    res => {
                        console.log(res)
                        this.articleList.push(res.data.posts)
                        console.log('=============')
                        this.scrollDisable = false
                    }
                )
            }
        }
    
    },
    directives: {
        compiledMarkdown: {
            bind: function(el) {
                el.innerHTML = marked(el.innerText)
                el.innerHTML = el.innerHTML.replace(/[^\u4e00-\u9fa5]/gi, '')

                if (el.querySelector('pre')) {
                    el.querySelector('pre').style.display = "none"
                }
                if (el.querySelector('blockquote')) {
                    el.querySelector('blockquote').style.display = "none"
                }
            }
        },
        scroll: {
            bind: function (el, binding){
              window.addEventListener('scroll', ()=> {
                console.log('......')
                if(document.body.scrollTop + window.innerHeight >= el.clientHeight) {
                    binding.value.call(this)
                    console.log('load data')
                }
              })
            }
        }
    },
}
</script>
<style scoped>
@import '../style/latestArticles.css';
</style>
