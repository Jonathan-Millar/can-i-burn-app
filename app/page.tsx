'use client'

import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Separator } from '@/components/ui/separator'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Loader2, Flame, MapPin, AlertTriangle, CheckCircle, Info } from 'lucide-react'

interface FireRestrictionData {
  latitude?: number
  longitude?: number
  province: string
  county?: string
  status?: string
  details?: string
  last_updated?: string
  error?: string
}

export default function HomePage() {
  const [location, setLocation] = useState('')
  const [latitude, setLatitude] = useState('')
  const [longitude, setLongitude] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<FireRestrictionData | null>(null)
  const [error, setError] = useState<string | null>(null)

  const getProvinceName = (code: string) => {
    const provinces: Record<string, string> = {
      'PE': 'Prince Edward Island',
      'NB': 'New Brunswick', 
      'NS': 'Nova Scotia',
      'ON': 'Ontario',
      'QC': 'Quebec',
      'NL': 'Newfoundland and Labrador',
      'BC': 'British Columbia',
      'AB': 'Alberta',
      'SK': 'Saskatchewan',
      'MB': 'Manitoba',
      'YT': 'Yukon Territory',
      'NT': 'Northwest Territories',
      'NU': 'Nunavut'
    }
    return provinces[code] || code
  }

  const getProvinceColor = (code: string) => {
    const colors: Record<string, string> = {
      'PE': 'bg-green-500',
      'NB': 'bg-blue-500',
      'NS': 'bg-yellow-500',
      'ON': 'bg-purple-500',
      'QC': 'bg-cyan-500',
      'NL': 'bg-pink-500',
      'BC': 'bg-purple-500',
      'AB': 'bg-orange-500',
      'SK': 'bg-green-500',
      'MB': 'bg-red-500',
      'YT': 'bg-teal-500',
      'NT': 'bg-red-500',
      'NU': 'bg-green-500'
    }
    return colors[code] || 'bg-gray-500'
  }

  const getStatusIcon = (status: string) => {
    if (status?.toLowerCase().includes('ban')) {
      return <AlertTriangle className="h-4 w-4" />
    } else if (status?.toLowerCase().includes('no') || status?.toLowerCase().includes('allowed')) {
      return <CheckCircle className="h-4 w-4" />
    }
    return <Info className="h-4 w-4" />
  }

  const getStatusVariant = (status: string) => {
    if (status?.toLowerCase().includes('ban')) {
      return 'destructive'
    } else if (status?.toLowerCase().includes('no') || status?.toLowerCase().includes('allowed')) {
      return 'default'
    }
    return 'secondary'
  }

  const checkFireRestrictions = async () => {
    // Validation
    if (!location && (!latitude || !longitude)) {
      setError('Please enter either a location name or both latitude and longitude coordinates.')
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      let url = '/api/enhanced/burn_restrictions?'
      
      if (location) {
        url += `location=${encodeURIComponent(location)}`
      } else {
        url += `latitude=${latitude}&longitude=${longitude}`
      }

      const response = await fetch(url)
      const data = await response.json()

      if (response.ok) {
        setResult(data)
      } else {
        setError(data.error || 'An error occurred while checking fire restrictions.')
      }
    } catch (error) {
      console.error('Error:', error)
      setError('Network error. Please check your connection and try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      checkFireRestrictions()
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-2xl mx-auto">
          {/* Header */}
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-orange-500 to-red-500 rounded-full mb-4">
              <Flame className="h-8 w-8 text-white" />
            </div>
            <h1 className="text-4xl font-bold text-gray-900 mb-2">
              Canada Fire Watch
            </h1>
            <p className="text-lg text-gray-600">
              Check current fire burn restrictions across all Canadian provinces and territories
            </p>
          </div>

          {/* Main Form Card */}
          <Card className="shadow-xl border-0 bg-white/80 backdrop-blur-sm">
            <CardHeader className="text-center pb-6">
              <CardTitle className="text-2xl text-gray-800">
                Check Fire Restrictions
              </CardTitle>
              <CardDescription className="text-gray-600">
                Enter a location name or coordinates to get current fire restriction status
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Location Name Input */}
              <div className="space-y-2">
                <Label htmlFor="location" className="text-sm font-medium text-gray-700">
                  Location Name
                </Label>
                <Input
                  id="location"
                  type="text"
                  placeholder="e.g., Vancouver, Toronto, Montreal, Halifax"
                  value={location}
                  onChange={(e) => setLocation(e.target.value)}
                  onKeyPress={handleKeyPress}
                  className="h-12 text-base"
                />
              </div>

              {/* Separator */}
              <div className="relative">
                <div className="absolute inset-0 flex items-center">
                  <Separator className="w-full" />
                </div>
                <div className="relative flex justify-center text-xs uppercase">
                  <span className="bg-white px-2 text-gray-500 font-medium">OR</span>
                </div>
              </div>

              {/* Coordinate Inputs */}
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="latitude" className="text-sm font-medium text-gray-700">
                    Latitude
                  </Label>
                  <Input
                    id="latitude"
                    type="number"
                    step="any"
                    placeholder="e.g., 46.3969"
                    value={latitude}
                    onChange={(e) => setLatitude(e.target.value)}
                    onKeyPress={handleKeyPress}
                    className="h-12 text-base"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="longitude" className="text-sm font-medium text-gray-700">
                    Longitude
                  </Label>
                  <Input
                    id="longitude"
                    type="number"
                    step="any"
                    placeholder="e.g., -63.7981"
                    value={longitude}
                    onChange={(e) => setLongitude(e.target.value)}
                    onKeyPress={handleKeyPress}
                    className="h-12 text-base"
                  />
                </div>
              </div>

              {/* Submit Button */}
              <Button
                onClick={checkFireRestrictions}
                disabled={loading}
                className="w-full h-12 text-base font-medium bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700"
              >
                {loading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Checking...
                  </>
                ) : (
                  <>
                    <MapPin className="mr-2 h-4 w-4" />
                    Check Fire Restrictions
                  </>
                )}
              </Button>
            </CardContent>
          </Card>

          {/* Error Display */}
          {error && (
            <Alert className="mt-6 border-red-200 bg-red-50">
              <AlertTriangle className="h-4 w-4 text-red-600" />
              <AlertDescription className="text-red-800">
                {error}
              </AlertDescription>
            </Alert>
          )}

          {/* Results Display */}
          {result && !result.error && (
            <Card className="mt-6 shadow-lg border-0 bg-white/80 backdrop-blur-sm">
              <CardHeader className="pb-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <Badge 
                      variant="secondary" 
                      className={`${getProvinceColor(result.province)} text-white border-0`}
                    >
                      {getProvinceName(result.province)} ({result.province})
                    </Badge>
                    {result.county && (
                      <Badge variant="outline" className="text-gray-700">
                        {result.county}
                      </Badge>
                    )}
                  </div>
                  {result.status && (
                    <Badge variant={getStatusVariant(result.status) as any}>
                      {getStatusIcon(result.status)}
                      <span className="ml-2">{result.status}</span>
                    </Badge>
                  )}
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                {result.details && (
                  <p className="text-gray-700 leading-relaxed">
                    {result.details}
                  </p>
                )}
                {result.last_updated && (
                  <div className="text-sm text-gray-500 border-t pt-4">
                    Last updated: {new Date(result.last_updated).toLocaleString()}
                  </div>
                )}
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  )
}
