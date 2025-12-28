"use client";

import React, { useState, useRef, useCallback } from 'react';
import { aiTryOnModel, TryOnRequest, TryOnResult } from '../services/aiTryOnModel';

interface AITryOnInterfaceProps {
  productImage?: string;
  productType?: 'top' | 'bottom' | 'dress' | 'outerwear' | 'shoes' | 'accessories';
  onClose?: () => void;
}

export default function AITryOnInterface({ 
  productImage, 
  productType = 'top', 
  onClose 
}: AITryOnInterfaceProps) {
  const [userImage, setUserImage] = useState<string>('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [result, setResult] = useState<TryOnResult | null>(null);
  const [error, setError] = useState<string>('');
  const [userGender, setUserGender] = useState<'male' | 'female'>('female');
  const [bodyMeasurements, setBodyMeasurements] = useState({
    height: '',
    chest: '',
    waist: '',
    hips: ''
  });
  const [showAdvanced, setShowAdvanced] = useState(false);
  
  const fileInputRef = useRef<HTMLInputElement>(null);
  const webcamRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [isWebcamActive, setIsWebcamActive] = useState(false);

  // Handle file upload
  const handleFileUpload = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        const result = e.target?.result as string;
        setUserImage(result);
        setError('');
      };
      reader.readAsDataURL(file);
    }
  }, []);

  // Start webcam
  const startWebcam = useCallback(async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ 
        video: { 
          width: 640, 
          height: 480,
          facingMode: 'user'
        } 
      });
      
      if (webcamRef.current) {
        webcamRef.current.srcObject = stream;
        webcamRef.current.play();
        setIsWebcamActive(true);
        setError('');
      }
    } catch (err) {
      setError('Failed to access webcam. Please upload an image instead.');
    }
  }, []);

  // Stop webcam
  const stopWebcam = useCallback(() => {
    if (webcamRef.current?.srcObject) {
      const stream = webcamRef.current.srcObject as MediaStream;
      stream.getTracks().forEach(track => track.stop());
      webcamRef.current.srcObject = null;
      setIsWebcamActive(false);
    }
  }, []);

  // Capture photo from webcam
  const capturePhoto = useCallback(() => {
    if (webcamRef.current && canvasRef.current) {
      const canvas = canvasRef.current;
      const video = webcamRef.current;
      
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      
      const ctx = canvas.getContext('2d');
      if (ctx) {
        ctx.drawImage(video, 0, 0);
        const imageData = canvas.toDataURL('image/jpeg', 0.8);
        setUserImage(imageData);
        stopWebcam();
      }
    }
  }, [stopWebcam]);

  // Process virtual try-on
  const processVirtualTryOn = useCallback(async () => {
    if (!userImage || !productImage) {
      setError('Please provide both user image and product image');
      return;
    }

    setIsProcessing(true);
    setError('');
    setResult(null);

    try {
      const request: TryOnRequest = {
        userImage,
        garmentImage: productImage,
        garmentType: productType,
        userGender,
        bodyMeasurements: {
          height: bodyMeasurements.height ? parseInt(bodyMeasurements.height) : undefined,
          chest: bodyMeasurements.chest ? parseInt(bodyMeasurements.chest) : undefined,
          waist: bodyMeasurements.waist ? parseInt(bodyMeasurements.waist) : undefined,
          hips: bodyMeasurements.hips ? parseInt(bodyMeasurements.hips) : undefined,
        }
      };

      const tryOnResult = await aiTryOnModel.processVirtualTryOn(request);
      setResult(tryOnResult);
      
      // Send training data to backend for continuous learning
      await sendTrainingData(request, tryOnResult);
      
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Processing failed');
    } finally {
      setIsProcessing(false);
    }
  }, [userImage, productImage, productType, userGender, bodyMeasurements]);

  // Send training data to backend
  const sendTrainingData = async (request: TryOnRequest, result: TryOnResult) => {
    try {
      await fetch('/api/ai-tryon/train', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          samples: [{
            input: {
              userImage: request.userImage,
              garmentImage: request.garmentImage,
              garmentType: request.garmentType,
              userGender: request.userGender
            },
            expected_output: result.processedImage,
            garment_type: request.garmentType,
            user_gender: request.userGender,
            quality_score: result.confidence
          }]
        })
      });
    } catch (err) {
      console.log('Training data upload failed:', err);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-xl max-w-6xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center">
              <span className="text-white text-xl">🤖</span>
            </div>
            <div>
              <h2 className="text-2xl font-bold text-gray-800">AI Virtual Try-On</h2>
              <p className="text-gray-600">See how this item looks on you with AI technology</p>
            </div>
          </div>
          {onClose && (
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600 text-2xl"
            >
              ×
            </button>
          )}
        </div>

        <div className="p-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Left Panel - Input */}
            <div className="space-y-6">
              <div>
                <h3 className="text-lg font-semibold text-gray-800 mb-4">Step 1: Upload Your Photo</h3>
                
                {/* Image Upload Options */}
                <div className="space-y-4">
                  <div className="flex gap-3">
                    <button
                      onClick={() => fileInputRef.current?.click()}
                      className="flex-1 bg-gradient-to-r from-blue-500 to-blue-600 text-white px-4 py-3 rounded-lg font-semibold hover:from-blue-600 hover:to-blue-700 transition-all"
                    >
                      📁 Upload Photo
                    </button>
                    <button
                      onClick={isWebcamActive ? stopWebcam : startWebcam}
                      className="flex-1 bg-gradient-to-r from-green-500 to-green-600 text-white px-4 py-3 rounded-lg font-semibold hover:from-green-600 hover:to-green-700 transition-all"
                    >
                      {isWebcamActive ? '🛑 Stop Camera' : '📷 Use Camera'}
                    </button>
                  </div>

                  <input
                    ref={fileInputRef}
                    type="file"
                    accept="image/*"
                    onChange={handleFileUpload}
                    className="hidden"
                  />

                  {/* Webcam */}
                  {isWebcamActive && (
                    <div className="relative">
                      <video
                        ref={webcamRef}
                        className="w-full rounded-lg"
                        autoPlay
                        muted
                      />
                      <button
                        onClick={capturePhoto}
                        className="absolute bottom-4 left-1/2 transform -translate-x-1/2 bg-white text-gray-800 px-6 py-2 rounded-full font-semibold shadow-lg hover:bg-gray-100 transition-all"
                      >
                        📸 Capture
                      </button>
                    </div>
                  )}

                  {/* User Image Preview */}
                  {userImage && (
                    <div className="relative">
                      <img
                        src={userImage}
                        alt="User"
                        className="w-full rounded-lg max-h-64 object-cover"
                      />
                      <button
                        onClick={() => setUserImage('')}
                        className="absolute top-2 right-2 bg-red-500 text-white rounded-full w-8 h-8 flex items-center justify-center hover:bg-red-600 transition-all"
                      >
                        ×
                      </button>
                    </div>
                  )}
                </div>
              </div>

              {/* User Preferences */}
              <div>
                <h3 className="text-lg font-semibold text-gray-800 mb-4">Step 2: Your Details</h3>
                
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Gender</label>
                    <div className="flex gap-3">
                      <button
                        onClick={() => setUserGender('female')}
                        className={`flex-1 px-4 py-2 rounded-lg font-semibold transition-all ${
                          userGender === 'female'
                            ? 'bg-gradient-to-r from-pink-500 to-pink-600 text-white'
                            : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                        }`}
                      >
                        👩 Female
                      </button>
                      <button
                        onClick={() => setUserGender('male')}
                        className={`flex-1 px-4 py-2 rounded-lg font-semibold transition-all ${
                          userGender === 'male'
                            ? 'bg-gradient-to-r from-blue-500 to-blue-600 text-white'
                            : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                        }`}
                      >
                        👨 Male
                      </button>
                    </div>
                  </div>

                  {/* Advanced Options */}
                  <div>
                    <button
                      onClick={() => setShowAdvanced(!showAdvanced)}
                      className="text-sm text-blue-600 hover:text-blue-700 font-medium"
                    >
                      {showAdvanced ? '▼' : '▶'} Advanced Options (Better Fit Analysis)
                    </button>
                    
                    {showAdvanced && (
                      <div className="mt-3 space-y-3 p-4 bg-gray-50 rounded-lg">
                        <div className="grid grid-cols-2 gap-3">
                          <div>
                            <label className="block text-xs font-medium text-gray-600 mb-1">Height (cm)</label>
                            <input
                              type="number"
                              value={bodyMeasurements.height}
                              onChange={(e) => setBodyMeasurements(prev => ({ ...prev, height: e.target.value }))}
                              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm"
                              placeholder="170"
                            />
                          </div>
                          <div>
                            <label className="block text-xs font-medium text-gray-600 mb-1">Chest (inches)</label>
                            <input
                              type="number"
                              value={bodyMeasurements.chest}
                              onChange={(e) => setBodyMeasurements(prev => ({ ...prev, chest: e.target.value }))}
                              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm"
                              placeholder="36"
                            />
                          </div>
                          <div>
                            <label className="block text-xs font-medium text-gray-600 mb-1">Waist (inches)</label>
                            <input
                              type="number"
                              value={bodyMeasurements.waist}
                              onChange={(e) => setBodyMeasurements(prev => ({ ...prev, waist: e.target.value }))}
                              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm"
                              placeholder="30"
                            />
                          </div>
                          <div>
                            <label className="block text-xs font-medium text-gray-600 mb-1">Hips (inches)</label>
                            <input
                              type="number"
                              value={bodyMeasurements.hips}
                              onChange={(e) => setBodyMeasurements(prev => ({ ...prev, hips: e.target.value }))}
                              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm"
                              placeholder="38"
                            />
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </div>

              {/* Product Preview */}
              {productImage && (
                <div>
                  <h3 className="text-lg font-semibold text-gray-800 mb-4">Product to Try On</h3>
                  <img
                    src={productImage}
                    alt="Product"
                    className="w-full rounded-lg max-h-48 object-cover"
                  />
                </div>
              )}

              {/* Try On Button */}
              <button
                onClick={processVirtualTryOn}
                disabled={!userImage || !productImage || isProcessing}
                className="w-full bg-gradient-to-r from-purple-500 to-pink-500 text-white px-6 py-4 rounded-lg font-bold text-lg hover:from-purple-600 hover:to-pink-600 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isProcessing ? (
                  <div className="flex items-center justify-center gap-3">
                    <div className="animate-spin rounded-full h-6 w-6 border-2 border-white border-t-transparent"></div>
                    Processing AI Try-On...
                  </div>
                ) : (
                  '🤖 Try It On with AI'
                )}
              </button>

              {/* Error Display */}
              {error && (
                <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                  <p className="text-red-700 text-sm">{error}</p>
                </div>
              )}
            </div>

            {/* Right Panel - Results */}
            <div className="space-y-6">
              <h3 className="text-lg font-semibold text-gray-800">AI Try-On Result</h3>
              
              {result ? (
                <div className="space-y-6">
                  {/* Result Image */}
                  <div className="relative">
                    <img
                      src={result.processedImage}
                      alt="Try-on result"
                      className="w-full rounded-lg shadow-lg"
                    />
                    <div className="absolute top-4 right-4 bg-black bg-opacity-70 text-white px-3 py-1 rounded-full text-sm">
                      Confidence: {(result.confidence * 100).toFixed(1)}%
                    </div>
                  </div>

                  {/* Fit Analysis */}
                  {result.fitAnalysis && (
                    <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                      <h4 className="font-semibold text-blue-800 mb-2">📏 Fit Analysis</h4>
                      <div className="space-y-2 text-sm">
                        <p><strong>Recommended Size:</strong> {result.fitAnalysis.size}</p>
                        <p><strong>Fit Quality:</strong> {(result.fitAnalysis.fitQuality * 100).toFixed(1)}%</p>
                        {result.fitAnalysis.adjustments && result.fitAnalysis.adjustments.length > 0 && (
                          <div>
                            <strong>Adjustments:</strong>
                            <ul className="list-disc list-inside mt-1">
                              {result.fitAnalysis.adjustments.map((adjustment, index) => (
                                <li key={index} className="text-blue-700">{adjustment}</li>
                              ))}
                            </ul>
                          </div>
                        )}
                      </div>
                    </div>
                  )}

                  {/* Recommendations */}
                  {result.recommendations && result.recommendations.length > 0 && (
                    <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                      <h4 className="font-semibold text-green-800 mb-2">💡 AI Recommendations</h4>
                      <ul className="space-y-1 text-sm">
                        {result.recommendations.map((recommendation, index) => (
                          <li key={index} className="text-green-700 flex items-start gap-2">
                            <span className="text-green-500 mt-0.5">•</span>
                            {recommendation}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Processing Stats */}
                  <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
                    <h4 className="font-semibold text-gray-800 mb-2">⚡ Processing Stats</h4>
                    <div className="text-sm text-gray-600 space-y-1">
                      <p>Processing Time: {result.processingTime.toFixed(0)}ms</p>
                      <p>AI Confidence: {(result.confidence * 100).toFixed(1)}%</p>
                      <p>Technology: Advanced Neural Network</p>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="flex items-center justify-center h-64 bg-gray-50 rounded-lg border-2 border-dashed border-gray-300">
                  <div className="text-center">
                    <div className="text-4xl mb-4">🤖</div>
                    <p className="text-gray-600">Upload your photo and click "Try It On" to see the AI magic!</p>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Hidden canvas for webcam capture */}
        <canvas ref={canvasRef} className="hidden" />
      </div>
    </div>
  );
}