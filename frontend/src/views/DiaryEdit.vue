<template>
  <div class="diary-edit">
    <el-header>
      <el-row :gutter="20">
        <el-col :span="12">
          <h1>{{ id ? '编辑日记' : '新增日记' }}</h1>
        </el-col>
        <el-col :span="12" class="header-buttons">
          <el-button @click="goBack">取消</el-button>
          <el-button type="primary" @click="saveDiary">保存</el-button>
        </el-col>
      </el-row>
    </el-header>
    <el-main>
      <el-form :model="diary" :rules="rules" ref="diaryForm" label-width="100px" class="diary-form">
        <el-form-item label="标题" prop="title">
          <el-input v-model="diary.title"></el-input>
        </el-form-item>
        <el-form-item label="内容" prop="content">
          <el-input type="textarea" v-model="diary.content" :rows="10"></el-input>
        </el-form-item>
        <el-form-item label="心情" prop="mood">
          <el-select v-model="diary.mood" placeholder="请选择心情">
            <el-option v-for="mood in moods" :key="mood" :label="mood" :value="mood"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="标签" prop="tags">
          <el-select v-model="diary.tags" multiple placeholder="请选择标签" style="width: 100%;">
            <el-option v-for="tag in tags" :key="tag" :label="tag" :value="tag"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="图片">
          <el-upload
            action="#"
            :auto-upload="false"
            :on-change="handleImageChange"
            :file-list="imageFileList"
            list-type="picture"
            :limit="1">
            <el-button slot="trigger" size="small" type="primary">选择图片</el-button>
            <div slot="tip" class="el-upload__tip">只能上传jpg/png文件，且不超过2MB</div>
          </el-upload>
        </el-form-item>
        <el-form-item label="录音">
          <el-button @click="startRecording" :disabled="isRecording">开始录音</el-button>
          <el-button @click="stopRecording" :disabled="!isRecording">停止录音</el-button>
          <audio v-if="audioUrl" :src="audioUrl" controls></audio>
          <div v-if="audioUrl" class="el-upload__tip">已录制音频，可重新录音覆盖</div>
        </el-form-item>
      </el-form>
    </el-main>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'DiaryEdit',
  data() {
    return {
      id: this.$route.params.id,
      diary: {
        title: '',
        content: '',
        mood: '',
        tags: []
      },
      rules: {
        title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
        content: [{ required: true, message: '请输入内容', trigger: 'blur' }],
        mood: [{ required: true, message: '请选择心情', trigger: 'change' }]
      },
      moods: ['开心', '难过', '平静', '愤怒', '焦虑'],
      tags: ['工作', '生活', '旅行', '学习', '家庭', '朋友'],
      imageFile: null,
      imageFileList: [],
      audioUrl: '',
      isRecording: false,
      mediaRecorder: null,
      audioChunks: [],
      darkMode: localStorage.getItem('darkMode') === 'true'
    }
  },
  mounted() {
    if (this.id) {
      this.fetchDiary()
    }
    this.applyTheme()
  },
  methods: {
    fetchDiary() {
      axios.get(`/api/diaries/${this.id}`).then(response => {
        const diaryData = response.data
        this.diary.title = diaryData[1]
        this.diary.content = diaryData[2]
        this.diary.mood = diaryData[3]
        this.diary.tags = diaryData[4].split(',').filter(tag => tag)
        if (diaryData[5]) {
          this.imageFileList = [{ name: '图片', url: diaryData[5] }]
        }
        if (diaryData[6]) {
          this.audioUrl = diaryData[6]
        }
      }).catch(error => {
        console.error('Error fetching diary:', error)
      })
    },
    handleImageChange(file, fileList) {
      this.imageFile = file.raw
      this.imageFileList = fileList
    },
    startRecording() {
      navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
          this.mediaRecorder = new MediaRecorder(stream)
          this.mediaRecorder.start()
          this.isRecording = true
          this.audioChunks = []
          this.mediaRecorder.addEventListener('dataavailable', event => {
            this.audioChunks.push(event.data)
          })
        })
        .catch(error => {
          console.error('Error accessing microphone:', error)
          this.$message.error('无法访问麦克风')
        })
    },
    stopRecording() {
      this.mediaRecorder.stop()
      this.isRecording = false
      this.mediaRecorder.addEventListener('stop', () => {
        const audioBlob = new Blob(this.audioChunks, { type: 'audio/webm' })
        this.audioUrl = URL.createObjectURL(audioBlob)
      })
    },
    saveDiary() {
      this.$refs.diaryForm.validate((valid) => {
        if (valid) {
          const formData = new FormData()
          formData.append('title', this.diary.title)
          formData.append('content', this.diary.content)
          formData.append('mood', this.diary.mood)
          formData.append('tags', this.diary.tags.join(','))
          if (this.imageFile) {
            formData.append('image', this.imageFile)
          }
          if (this.audioUrl && this.audioChunks.length > 0) {
            const audioBlob = new Blob(this.audioChunks, { type: 'audio/webm' })
            formData.append('audio', audioBlob, 'recording.webm')
          }
          if (this.id) {
            axios.put(`/api/diaries/${this.id}`, formData).then(() => {
              this.$message.success('更新成功')
              this.$router.push({ name: 'DiaryDetail', params: { id: this.id } })
            }).catch(error => {
              console.error('Error updating diary:', error)
              this.$message.error('更新失败')
            })
          } else {
            axios.post('/api/diaries', formData).then(() => {
              this.$message.success('保存成功')
              this.$router.push({ name: 'DiaryList' })
            }).catch(error => {
              console.error('Error creating diary:', error)
              this.$message.error('保存失败')
            })
          }
        }
      })
    },
    goBack() {
      this.$router.push({ name: 'DiaryList' })
    },
    applyTheme() {
      if (this.darkMode) {
        document.body.classList.add('dark-mode')
      } else {
        document.body.classList.remove('dark-mode')
      }
    }
  }
}
</script>

<style scoped>
.diary-edit {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}
.header-buttons {
  display: flex;
  justify-content: flex-end;
  align-items: center;
}
.diary-form {
  text-align: left;
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
  .diary-form .el-form-item label {
    font-size: 14px;
  }
  .diary-form .el-input, .diary-form .el-select, .diary-form .el-textarea {
    font-size: 14px;
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
    padding: 6px 10px;
    font-size: 12px;
  }
  .diary-form .el-form-item label {
    font-size: 12px;
  }
  .diary-form .el-input, .diary-form .el-select, .diary-form .el-textarea {
    font-size: 12px;
  }
  .diary-form .el-form-item {
    margin-bottom: 10px;
  }
  .diary-edit {
    padding: 10px;
  }
  .diary-form {
    label-width: 80px;
  }
}
</style>
