import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';

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

  const handlePatientSelect = (patient: any) => {
    setSelectedPatient(patient);
    setPatientReport('');
    setTreatmentPlan('');
  };

  const handleGenerateReport = () => {
    if (selectedPatient) {
      const report = generatePatientReport(selectedPatient);
      setPatientReport(report);
    }
  };

  const handleSuggestTreatment = () => {
    if (selectedPatient) {
      const plan = suggestTreatmentPlan(selectedPatient);
      setTreatmentPlan(plan);
    }
  };

  return (
    <div className="p-4 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">MediMind Demo App</h1>
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
              <Button onClick={handleGenerateReport} className="mr-2">Generate Report</Button>
              <Button onClick={handleSuggestTreatment}>Suggest Treatment</Button>
            </CardContent>
          </Card>
          {patientReport && (
            <Card>
              <CardHeader>
                <CardTitle>Patient Report</CardTitle>
              </CardHeader>
              <CardContent>
                <pre className="whitespace-pre-wrap">{patientReport}</pre>
              </CardContent>
            </Card>
          )}
          {treatmentPlan && (
            <Card>
              <CardHeader>
                <CardTitle>Suggested Treatment Plan</CardTitle>
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
