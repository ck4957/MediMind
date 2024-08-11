import React, { useState } from 'react';
import { Button } from '@/src/ui/button';
import { Card, CardHeader, CardContent } from '@/src/ui/card';
import { Alert, AlertDescription } from '@/src/ui/alert';

export const HealthReadingsUI = () => {
  const [pulse, setPulse] = useState('');
  const [systolic, setSystolic] = useState('');
  const [diastolic, setDiastolic] = useState('');
  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState('');

  const takeReading = () => {
    // Simulating a reading for demonstration purposes
    setPulse( (Math.floor(Math.random() * (100 - 60) + 60)).toString());
    setSystolic((Math.floor(Math.random() * (140 - 90) + 90)).toString());
    setDiastolic((Math.floor(Math.random() * (90 - 60) + 60)).toString());
  };

  const connectBluetooth = async () => {
    if (!(navigator as any).bluetooth) {
      setError("Bluetooth is not supported in this browser.");
      return;
    }

    try {
      const device = await (navigator as any).bluetooth.requestDevice({
        filters: [{ services: ['heart_rate'] }]
      });
      const server = await device.gatt.connect();
      setIsConnected(true);
      setError('');
      // Here you would typically set up listeners for incoming data
      // and handle the actual reading of data from the device
    } catch (error) {
      setError(`Bluetooth Error: ${(error as any).message}`);
    }
  };

  return (
    <div className="p-4">
      <Card className="w-full max-w-md mx-auto">
        <CardHeader className="text-2xl font-bold text-center">Health Readings</CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="text-center">
              <p className="text-lg">Pulse: {pulse ? `${pulse} bpm` : 'N/A'}</p>
              <p className="text-lg">Blood Pressure: {systolic && diastolic ? `${systolic}/${diastolic} mmHg` : 'N/A'}</p>
            </div>
            <Button onClick={takeReading} className="w-full">Take Reading</Button>
            <Button 
              onClick={connectBluetooth} 
              className="w-full"
              disabled={isConnected}
            >
              {isConnected ? 'Connected' : 'Connect Bluetooth Device'}
            </Button>
            {error && (
              <Alert variant="destructive">
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};
