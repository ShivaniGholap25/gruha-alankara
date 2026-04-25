import { Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Footer from './components/Footer'
import BuddyChat from './components/BuddyChat'
import ProtectedRoute from './components/ProtectedRoute'
import HomePage from './pages/HomePage'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import DashboardPage from './pages/DashboardPage'
import DesignStudioPage from './pages/DesignStudioPage'
import AnalyzeRoomPage from './pages/AnalyzeRoomPage'
import CatalogPage from './pages/CatalogPage'
import FurniturePage from './pages/FurniturePage'
import MyBookingsPage from './pages/MyBookingsPage'
import StyleQuizPage from './pages/StyleQuizPage'
import BudgetCalcPage from './pages/BudgetCalcPage'
import GalleryPage from './pages/GalleryPage'
import NearbyShopsPage from './pages/NearbyShopsPage'
import LiveARPage from './pages/LiveARPage'

export default function App() {
  return (
    <>
      <Navbar />
      <main style={{ flex: 1 }}>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/dashboard" element={<ProtectedRoute><DashboardPage /></ProtectedRoute>} />
          <Route path="/design" element={<DesignStudioPage />} />
          <Route path="/analyze" element={<AnalyzeRoomPage />} />
          <Route path="/catalog" element={<ProtectedRoute><CatalogPage /></ProtectedRoute>} />
          <Route path="/furniture" element={<FurniturePage />} />
          <Route path="/my-bookings" element={<ProtectedRoute><MyBookingsPage /></ProtectedRoute>} />
          <Route path="/style-quiz" element={<StyleQuizPage />} />
          <Route path="/budget-calculator" element={<BudgetCalcPage />} />
          <Route path="/gallery" element={<GalleryPage />} />
          <Route path="/nearby-shops" element={<NearbyShopsPage />} />
          <Route path="/live-ar" element={<LiveARPage />} />
        </Routes>
      </main>
      <Footer />
      <BuddyChat />
    </>
  )
}
