import { useState } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { 
  BookOpen, 
  Upload, 
  BarChart3, 
  Settings, 
  FileText, 
  Target,
  TrendingUp,
  Users,
  CheckCircle,
  AlertCircle
} from 'lucide-react'
import './App.css'

// Components
import Navigation from './components/Navigation'
import Dashboard from './components/Dashboard'
import PLOManagement from './components/PLOManagement'
import CLOManagement from './components/CLOManagement'
import DocumentUpload from './components/DocumentUpload'
import AssessmentResults from './components/AssessmentResults'

function App() {
  const [activeTab, setActiveTab] = useState('dashboard')

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-6">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">
                Nền tảng đánh giá CLO/PLO
              </h1>
              <p className="text-gray-600">
                Khoa Cơ khí - Trường Đại học Công nghệ Đông Á (EAUT)
              </p>
            </div>
            <div className="flex items-center space-x-2">
              <Badge variant="secondary" className="bg-green-100 text-green-800">
                <CheckCircle className="w-4 h-4 mr-1" />
                Hệ thống hoạt động
              </Badge>
            </div>
          </div>
        </div>

        {/* Main Content */}
        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid w-full grid-cols-5 mb-6">
            <TabsTrigger value="dashboard" className="flex items-center space-x-2">
              <BarChart3 className="w-4 h-4" />
              <span>Dashboard</span>
            </TabsTrigger>
            <TabsTrigger value="plo" className="flex items-center space-x-2">
              <Target className="w-4 h-4" />
              <span>PLO</span>
            </TabsTrigger>
            <TabsTrigger value="clo" className="flex items-center space-x-2">
              <BookOpen className="w-4 h-4" />
              <span>CLO</span>
            </TabsTrigger>
            <TabsTrigger value="upload" className="flex items-center space-x-2">
              <Upload className="w-4 h-4" />
              <span>Tải tài liệu</span>
            </TabsTrigger>
            <TabsTrigger value="results" className="flex items-center space-x-2">
              <FileText className="w-4 h-4" />
              <span>Kết quả</span>
            </TabsTrigger>
          </TabsList>

          <TabsContent value="dashboard">
            <Dashboard />
          </TabsContent>

          <TabsContent value="plo">
            <PLOManagement />
          </TabsContent>

          <TabsContent value="clo">
            <CLOManagement />
          </TabsContent>

          <TabsContent value="upload">
            <DocumentUpload />
          </TabsContent>

          <TabsContent value="results">
            <AssessmentResults />
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}

export default App

