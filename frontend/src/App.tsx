import { Routes, Route } from 'react-router-dom'
import Layout from './components/layout/Layout'
import HomePage from './pages/HomePage'
import ModulesPage from './pages/ModulesPage'
import TopicPage from './pages/TopicPage'
import GamePage from './pages/GamePage'
import NotFoundPage from './pages/NotFoundPage'

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<HomePage />} />
        <Route path="modules" element={<ModulesPage />} />
        <Route path="modules/:moduleId/:topicId" element={<TopicPage />} />
        <Route path="game" element={<GamePage />} />
        <Route path="*" element={<NotFoundPage />} />
      </Route>
    </Routes>
  )
}

export default App
