<template>
  <div class="diary-detail">
    <el-header>
      <el-row :gutter="20">
        <el-col :span="12">
          <h1>{{ diary[1] }}</h1>
        </el-col>
        <el-col :span="12" class="header-buttons">
          <el-button @click="goBack">返回</el-button>
          <el-button type="primary" @click="goToEdit">编辑</el-button>
          <el-button type="danger" @click="deleteDiary">删除</el-button>
        </el-col>
      </el-row>
    </el-header>
    <el-main>
      <el-card>
        <p class="date">{{ formatDate(diary[7]) }}</p>
        <p class="mood">心情：{{ diary[3] }}</p>
        <p class="tags">标签：{{ diary[4] }}</p>
        <div class="content">{{ diary[2] }}</div>
        <div v-if="diary[5]" class="media">
          <h3>图片</h3>
          <img :src="diary[5]" alt="日记图片" style="max-width: 100%; max-height: 300px;">
        </div>
        <div v-if="diary[6]" class="media">
          <h3>录音</h3>
          <audio controls :src="diary[6]"></audio>
        </div>
      </el-card>
    </el-main>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'DiaryDetail',
  data() {
    return {
      diary: []
    }
  },
  mounted() {
    this.fetchDiary()
  },
  methods: {
    fetchDiary() {
      const id = this.$route.params.id
      axios.get(`/api/diaries/${id}`).then(response => {
        this.diary = response.data
      }).catch(error => {
        console.error('Error fetching diary:', error)
      })
    },
    goBack() {
      this.$router.push({ name: 'DiaryList' })
    },
    goToEdit() {
      this.$router.push({ name: 'DiaryEdit', params: { id: this.$route.params.id } })
    },
    deleteDiary() {
      const id = this.$route.params.id
      axios.delete(`/api/diaries/${id}`).then(() => {
        this.$message.success('删除成功')
        this.$router.push({ name: 'DiaryList' })
      }).catch(error => {
        console.error('Error deleting diary:', error)
        this.$message.error('删除失败')
      })
    },
    formatDate(dateStr) {
      const date = new Date(dateStr)
      return date.toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' })
    }
  }
}
</script>

<style scoped>
.diary-detail {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}
.header-buttons {
  display: flex;
  justify-content: flex-end;
  align-items: center;
}
.date {
  color: #909399;
  font-size: 14px;
}
.mood, .tags {
  font-size: 14px;
  color: #909399;
}
.content {
  margin-top: 20px;
  font-size: 16px;
  line-height: 1.6;
  text-align: left;
}
.media {
  margin-top: 20px;
}
.media h3 {
  margin-top: 0;
  font-size: 18px;
}
@media (max-width: 768px) {
  .header-buttons {
    justify-content: flex-start;
    margin-top: 10px;
    flex-wrap: wrap;
  }
  .header-buttons .el-button {
    margin-bottom: 5px;
    padding: 8px 12px;
    font-size: 14px;
  }
  .content {
    font-size: 14px;
    margin-top: 15px;
  }
  .media {
    margin-top: 15px;
  }
  .media h3 {
    font-size: 16px;
  }
  img {
    max-height: 200px;
  }
  .el-row {
    display: flex;
    flex-direction: column;
  }
  .el-col {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .header-buttons .el-button {
    padding: 12px 16px;
    font-size: 16px;
    min-width: 60px;
    min-height: 48px;
    border-radius: 24px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    margin: 4px;
    z-index: 100;
  }
  .content {
    font-size: 14px;
    margin-top: 12px;
    line-height: 1.6;
    color: #444;
  }
  .date, .mood, .tags {
    font-size: 13px;
    color: #666;
  }
  .media {
    margin-top: 12px;
  }
  .media h3 {
    font-size: 15px;
    color: #333;
  }
  img {
    max-height: 180px;
    border-radius: 8px;
  }
  .diary-detail {
    padding: 12px;
    background: #fff;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  }
}
</style>
