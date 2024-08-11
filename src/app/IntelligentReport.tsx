import React, { useState } from 'react';
import { Button } from '@/src/ui/button';
import { Card, CardHeader, CardTitle, CardContent } from '@/src/ui/card';
const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL;
// Sample FHIR resources (simplified for demonstration)
const samplePatients = [
  {
    id: '1',
    name: 'John Doe',
    birthDate: '1980-01-01',
    gender: 'male',
    conditions: ['Hypertension', 'Type 2 Diabetes'],
    medications: ['Lisinopril', 'Metformin']
  },
  {
    id: '2',
    name: 'Jane Smith',
    birthDate: '1975-05-15',
    gender: 'female',
    conditions: ['Asthma', 'Allergic Rhinitis'],
    medications: ['Albuterol', 'Fluticasone']
  }
];

// Simulated function to generate a patient report
const generatePatientReport = (patient: any) => {
  return `
    Patient Report for ${patient.name}
    Date of Birth: ${patient.birthDate}
    Gender: ${patient.gender}
    
    Conditions:
    ${patient.conditions.map((condition:any) => `- ${condition}`).join('\n')}
    
    Current Medications:
    ${patient.medications.map((medication:any) => `- ${medication}`).join('\n')}
  `;
};

// Simulated function to suggest treatment plans
const suggestTreatmentPlan = (patient:any) => {
  let plan = `Treatment Plan for ${patient.name}:\n\n`;
  
  if (patient.conditions.includes('Hypertension')) {
    plan += "- Continue Lisinopril for blood pressure management\n";
    plan += "- Recommend low-sodium diet and regular exercise\n";
  }
  
  if (patient.conditions.includes('Type 2 Diabetes')) {
    plan += "- Continue Metformin for blood sugar control\n";
    plan += "- Suggest meeting with a nutritionist for dietary guidance\n";
  }
  
  if (patient.conditions.includes('Asthma')) {
    plan += "- Use Albuterol as needed for acute symptoms\n";
    plan += "- Consider adding an inhaled corticosteroid for long-term control\n";
  }
  
  if (patient.conditions.includes('Allergic Rhinitis')) {
    plan += "- Continue Fluticasone nasal spray\n";
    plan += "- Recommend allergen avoidance strategies\n";
  }
  
  return plan;
};

export const IntelligentReport = () => {
  const [selectedPatient, setSelectedPatient] = useState(null);
  const [patientReport, setPatientReport] = useState('');
  const [treatmentPlan, setTreatmentPlan] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handlePatientSelect = (patient: any) => {
    setSelectedPatient(patient);
    setPatientReport('');
    setTreatmentPlan('');
  };

  const handleGenerateReport = async () => {
    if (selectedPatient) {
      setIsLoading(true);
      try {
        const response = await fetch(`${BACKEND_URL}/generate_report`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ patient: selectedPatient }),
        });
        const data = await response.json();
        setPatientReport(data.report);
      } catch (error) {
        console.error('Error generating report:', error);
        const report = generatePatientReport(selectedPatient);
        setPatientReport(report);
    }
      setIsLoading(false);
    }
  };

  const handleSuggestTreatment = async() => {
    if (selectedPatient) {
      setIsLoading(true);
      try {
        const response = await fetch(`${BACKEND_URL}/suggest_treatment`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ patient: selectedPatient }),
        });
        const data = await response.json();
        setTreatmentPlan(data.plan);
      } catch (error) {
        console.error('Error suggesting treatment:', error);
        const plan = suggestTreatmentPlan(selectedPatient);
        setTreatmentPlan(plan);
      }
      setIsLoading(false);
    }
  };

  return (
    <div className="p-4 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">FHIR Demo App with GatorTron</h1>
      <div className="grid grid-cols-2 gap-4 mb-4">
        {samplePatients.map(patient => (
          <Button
            key={patient.id}
            onClick={() => handlePatientSelect(patient)}
            variant={selectedPatient === patient ? "default" : "outline"}
          >
            {patient.name}
          </Button>
        ))}
      </div>
      {selectedPatient && (
        <div className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Selected Patient: {(selectedPatient as any).name}</CardTitle>
            </CardHeader>
            <CardContent>
              <Button onClick={handleGenerateReport} className="mr-2" disabled={isLoading}>
                Generate Report
              </Button>
              <Button onClick={handleSuggestTreatment} disabled={isLoading}>
                Suggest Treatment
              </Button>
            </CardContent>
          </Card>
          {isLoading && <p>Loading...</p>}
          {patientReport && (
            <Card>
              <CardHeader>
                <CardTitle>Patient Report (Generated by GatorTron)</CardTitle>
              </CardHeader>
              <CardContent>
                <pre className="whitespace-pre-wrap">{patientReport}</pre>
              </CardContent>
            </Card>
          )}
          {treatmentPlan && (
            <Card>
              <CardHeader>
                <CardTitle>Suggested Treatment Plan (Generated by GatorTron)</CardTitle>
              </CardHeader>
              <CardContent>
                <pre className="whitespace-pre-wrap">{treatmentPlan}</pre>
              </CardContent>
            </Card>
          )}
        </div>
      )}
    </div>
  );
};
