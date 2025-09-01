import { useState, useCallback } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Label } from '@/components/ui/label.jsx'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { Alert, AlertDescription } from '@/components/ui/alert.jsx'
import { 
  Upload, 
  FileText, 
  CheckCircle, 
  AlertCircle, 
  Clock,
  X,
  Eye,
  Download,
  BarChart3
} from 'lucide-react'

const DocumentUpload = () => {
  const [files, setFiles] = useState([])
  const [uploading, setUploading] = useState(false)
  const [dragActive, setDragActive] = useState(false)
  const [selectedCourse, setSelectedCourse] = useState('')
  const [documentType, setDocumentType] = useState('assignment')

  const courses = [
    { code: 'ME2252', name: 'Vẽ kỹ thuật' },
    { code: 'ME2205', name: 'Cơ học kỹ thuật' },
    { code: 'AET3217', name: 'Kết cấu tính toán ô tô' },
    { code: 'AET3218', name: 'Cấu tạo ô tô' }
  ]

  const documentTypes = [
    { value: 'assignment', label: 'Bài tập' },
    { value: 'exam', label: 'Bài kiểm tra' },
    { value: 'project', label: 'Đồ án' },
    { value: 'report', label: 'Báo cáo' },
    { value: 'thesis', label: 'Luận văn' }
  ]

  // Handle drag events
  const handleDrag = useCallback((e) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true)
    } else if (e.type === "dragleave") {
      setDragActive(false)
    }
  }, [])

  // Handle drop
  const handleDrop = useCallback((e) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFiles(e.dataTransfer.files)
    }
  }, [])

  // Handle file selection
  const handleFileSelect = (e) => {
    if (e.target.files) {
      handleFiles(e.target.files)
    }
  }

  // Process selected files
  const handleFiles = (fileList) => {
    const newFiles = Array.from(fileList).map(file => ({
      id: Math.random().toString(36).substr(2, 9),
      file: file,
      name: file.name,
      size: file.size,
      type: file.type,
      status: 'pending', // pending, uploading, uploaded, processing, completed, error
      progress: 0,
      results: null,
      error: null
    }))
    
    setFiles(prev => [...prev, ...newFiles])
  }

  // Remove file
  const removeFile = (fileId) => {
    setFiles(prev => prev.filter(f => f.id !== fileId))
  }

  // Upload and process files
  const handleUpload = async () => {
    if (!selectedCourse) {
      alert('Vui lòng chọn môn học')
      return
    }

    setUploading(true)
    
    for (const fileItem of files.filter(f => f.status === 'pending')) {
      try {
        // Update status to uploading
        setFiles(prev => prev.map(f => 
          f.id === fileItem.id ? { ...f, status: 'uploading', progress: 0 } : f
        ))

        // Simulate upload progress
        for (let progress = 0; progress <= 100; progress += 10) {
          await new Promise(resolve => setTimeout(resolve, 100))
          setFiles(prev => prev.map(f => 
            f.id === fileItem.id ? { ...f, progress } : f
          ))
        }

        // Simulate file upload to backend
        const formData = new FormData()
        formData.append('file', fileItem.file)
        formData.append('course_code', selectedCourse)
        formData.append('document_type', documentType)

        // In real implementation, this would be actual API call
        // const response = await fetch('http://localhost:5001/api/documents/upload', {
        //   method: 'POST',
        //   body: formData
        // })
        // const uploadResult = await response.json()

        // Simulate successful upload
        setFiles(prev => prev.map(f => 
          f.id === fileItem.id ? { ...f, status: 'uploaded', progress: 100 } : f
        ))

        // Simulate processing
        await new Promise(resolve => setTimeout(resolve, 1000))
        setFiles(prev => prev.map(f => 
          f.id === fileItem.id ? { ...f, status: 'processing' } : f
        ))

        // Simulate assessment completion
        await new Promise(resolve => setTimeout(resolve, 2000))
        
        // Mock assessment results
        const mockResults = {
          clo_results: [
            { clo_code: 'CLO1', score: 3.2, confidence: 0.85 },
            { clo_code: 'CLO2', score: 2.8, confidence: 0.78 },
            { clo_code: 'CLO3', score: 3.5, confidence: 0.92 },
            { clo_code: 'CLO4', score: 3.8, confidence: 0.88 }
          ],
          plo_scores: {
            'PLO4': { score: 3.0, confidence: 0.82 },
            'PLO10': { score: 3.5, confidence: 0.92 },
            'PLO12': { score: 3.8, confidence: 0.88 }
          }
        }

        setFiles(prev => prev.map(f => 
          f.id === fileItem.id ? { 
            ...f, 
            status: 'completed', 
            results: mockResults 
          } : f
        ))

      } catch (error) {
        setFiles(prev => prev.map(f => 
          f.id === fileItem.id ? { 
            ...f, 
            status: 'error', 
            error: error.message 
          } : f
        ))
      }
    }
    
    setUploading(false)
  }

  // Get file size in readable format
  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  // Get status badge
  const getStatusBadge = (status) => {
    const statusConfig = {
      pending: { label: 'Chờ xử lý', color: 'bg-gray-100 text-gray-800', icon: Clock },
      uploading: { label: 'Đang tải lên', color: 'bg-blue-100 text-blue-800', icon: Upload },
      uploaded: { label: 'Đã tải lên', color: 'bg-green-100 text-green-800', icon: CheckCircle },
      processing: { label: 'Đang đánh giá', color: 'bg-yellow-100 text-yellow-800', icon: BarChart3 },
      completed: { label: 'Hoàn thành', color: 'bg-green-100 text-green-800', icon: CheckCircle },
      error: { label: 'Lỗi', color: 'bg-red-100 text-red-800', icon: AlertCircle }
    }
    
    const config = statusConfig[status] || statusConfig.pending
    const Icon = config.icon
    
    return (
      <Badge className={config.color}>
        <Icon className="w-3 h-3 mr-1" />
        {config.label}
      </Badge>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Tải tài liệu đánh giá</h2>
        <p className="text-gray-600">
          Tải lên tài liệu để đánh giá mức độ đạt chuẩn đầu ra CLO/PLO
        </p>
      </div>

      {/* Upload Configuration */}
      <Card>
        <CardHeader>
          <CardTitle>Cấu hình đánh giá</CardTitle>
          <CardDescription>
            Chọn môn học và loại tài liệu trước khi tải lên
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <Label htmlFor="course">Môn học</Label>
              <Select value={selectedCourse} onValueChange={setSelectedCourse}>
                <SelectTrigger>
                  <SelectValue placeholder="Chọn môn học" />
                </SelectTrigger>
                <SelectContent>
                  {courses.map((course) => (
                    <SelectItem key={course.code} value={course.code}>
                      {course.code} - {course.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label htmlFor="docType">Loại tài liệu</Label>
              <Select value={documentType} onValueChange={setDocumentType}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {documentTypes.map((type) => (
                    <SelectItem key={type.value} value={type.value}>
                      {type.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* File Upload Area */}
      <Card>
        <CardHeader>
          <CardTitle>Tải tài liệu</CardTitle>
          <CardDescription>
            Hỗ trợ các định dạng: PDF, DOC, DOCX, TXT (tối đa 50MB)
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div
            className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
              dragActive 
                ? 'border-blue-500 bg-blue-50' 
                : 'border-gray-300 hover:border-gray-400'
            }`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
          >
            <Upload className="mx-auto h-12 w-12 text-gray-400 mb-4" />
            <div className="space-y-2">
              <p className="text-lg font-medium text-gray-900">
                Kéo thả tài liệu vào đây
              </p>
              <p className="text-gray-500">hoặc</p>
              <div>
                <input
                  type="file"
                  multiple
                  accept=".pdf,.doc,.docx,.txt"
                  onChange={handleFileSelect}
                  className="hidden"
                  id="file-upload"
                />
                <label htmlFor="file-upload">
                  <Button variant="outline" className="cursor-pointer">
                    Chọn tệp tin
                  </Button>
                </label>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* File List */}
      {files.length > 0 && (
        <Card>
          <CardHeader>
            <div className="flex justify-between items-center">
              <div>
                <CardTitle>Danh sách tài liệu</CardTitle>
                <CardDescription>
                  {files.length} tệp tin đã chọn
                </CardDescription>
              </div>
              <Button 
                onClick={handleUpload}
                disabled={uploading || !selectedCourse || files.filter(f => f.status === 'pending').length === 0}
              >
                {uploading ? 'Đang xử lý...' : 'Bắt đầu đánh giá'}
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {files.map((fileItem) => (
                <div key={fileItem.id} className="border rounded-lg p-4">
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center space-x-3">
                      <FileText className="h-8 w-8 text-blue-500" />
                      <div>
                        <p className="font-medium">{fileItem.name}</p>
                        <p className="text-sm text-gray-500">
                          {formatFileSize(fileItem.size)}
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      {getStatusBadge(fileItem.status)}
                      {fileItem.status === 'pending' && (
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => removeFile(fileItem.id)}
                        >
                          <X className="h-4 w-4" />
                        </Button>
                      )}
                    </div>
                  </div>
                  
                  {/* Progress Bar */}
                  {(fileItem.status === 'uploading' || fileItem.status === 'processing') && (
                    <div className="mb-2">
                      <Progress value={fileItem.progress} className="h-2" />
                      <p className="text-xs text-gray-500 mt-1">
                        {fileItem.status === 'uploading' 
                          ? `Đang tải lên... ${fileItem.progress}%`
                          : 'Đang phân tích và đánh giá...'
                        }
                      </p>
                    </div>
                  )}

                  {/* Error Message */}
                  {fileItem.status === 'error' && (
                    <Alert className="mt-2">
                      <AlertCircle className="h-4 w-4" />
                      <AlertDescription>
                        Lỗi: {fileItem.error}
                      </AlertDescription>
                    </Alert>
                  )}

                  {/* Results Preview */}
                  {fileItem.status === 'completed' && fileItem.results && (
                    <div className="mt-3 p-3 bg-green-50 rounded-lg">
                      <h4 className="font-medium text-green-800 mb-2">Kết quả đánh giá</h4>
                      <div className="grid grid-cols-2 gap-4 text-sm">
                        <div>
                          <p className="font-medium text-green-700">CLO Scores:</p>
                          {fileItem.results.clo_results.map((clo, index) => (
                            <div key={index} className="flex justify-between">
                              <span>{clo.clo_code}:</span>
                              <span className="font-medium">{clo.score.toFixed(1)}/4.0</span>
                            </div>
                          ))}
                        </div>
                        <div>
                          <p className="font-medium text-green-700">PLO Scores:</p>
                          {Object.entries(fileItem.results.plo_scores).map(([plo, data]) => (
                            <div key={plo} className="flex justify-between">
                              <span>{plo}:</span>
                              <span className="font-medium">{data.score.toFixed(1)}/4.0</span>
                            </div>
                          ))}
                        </div>
                      </div>
                      <div className="flex space-x-2 mt-3">
                        <Button variant="outline" size="sm">
                          <Eye className="w-4 h-4 mr-1" />
                          Xem chi tiết
                        </Button>
                        <Button variant="outline" size="sm">
                          <Download className="w-4 h-4 mr-1" />
                          Tải báo cáo
                        </Button>
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Instructions */}
      <Card>
        <CardHeader>
          <CardTitle>Hướng dẫn sử dụng</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3 text-sm text-gray-600">
            <div className="flex items-start space-x-2">
              <div className="w-6 h-6 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center text-xs font-bold">1</div>
              <p>Chọn môn học và loại tài liệu phù hợp</p>
            </div>
            <div className="flex items-start space-x-2">
              <div className="w-6 h-6 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center text-xs font-bold">2</div>
              <p>Tải lên tài liệu (PDF, DOC, DOCX, TXT) - tối đa 50MB mỗi tệp</p>
            </div>
            <div className="flex items-start space-x-2">
              <div className="w-6 h-6 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center text-xs font-bold">3</div>
              <p>Hệ thống sẽ tự động phân tích nội dung và đánh giá mức độ đạt CLO/PLO</p>
            </div>
            <div className="flex items-start space-x-2">
              <div className="w-6 h-6 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center text-xs font-bold">4</div>
              <p>Xem kết quả chi tiết và tải báo cáo đánh giá</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default DocumentUpload

