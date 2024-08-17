import React, { useState } from 'react';
import { Alert, AlertDescription, AlertTitle } from '@/src/ui/alert';
const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL;


export const NoteFhir = () => {
  const [note, setNote] = useState('');
  const [fhir, setFhir] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e:any) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setFhir('');

    try {
      const response = await fetch(`${BACKEND_URL}/convert`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ note }),
      });
      let data = sampleFhir;
      if (!response.ok) {
         console.log('Failed to convert note to FHIR');
      } else {
        data = await response.json();
      }
      setFhir(JSON.stringify(data, null, 2));
    } catch (err:any) {
      setError(err.message);
      setFhir(JSON.stringify(sampleFhir, null, 2));

    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Note-to-FHIR Converter</h1>
      <form onSubmit={handleSubmit} className="mb-4">
        <textarea
          className="w-full p-2 border rounded"
          rows={10}
          value={note}
          onChange={(e) => setNote(e.target.value)}
          placeholder="Enter clinical note here..."
        />
        <button
          type="submit"
          className="mt-2 px-4 py-2 bg-blue-500 text-white rounded"
          disabled={loading}
        >
          {loading ? 'Converting...' : 'Convert to FHIR'}
        </button>
      </form>
      {error && (
        <Alert variant="destructive">
          <AlertTitle>Error</AlertTitle>
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}
      {fhir && (
        <div>
          <h2 className="text-xl font-bold mb-2">FHIR Result:</h2>
          <pre className="bg-gray-100 p-4 rounded overflow-x-auto">
            <code>{fhir}</code>
          </pre>
        </div>
      )}
    </div>
  );
};

export const sampleFhir = {
    "resourceType" : "Patient",
    "id" : "example",
    "identifier" : [{
      "use" : "usual",
      "type" : {
        "coding" : [{
          "system" : "http://terminology.hl7.org/CodeSystem/v2-0203",
          "code" : "MR"
        }]
      },
      "system" : "urn:oid:1.2.36.146.595.217.0.1",
      "value" : "12345",
      "period" : {
        "start" : "2001-05-06"
      },
      "assigner" : {
        "display" : "Acme Healthcare"
      }
    }],
    "active" : true,
    "name" : [{
      "use" : "official",
      "family" : "Chalmers",
      "given" : ["Peter",
      "James"]
    },
    {
      "use" : "usual",
      "given" : ["Jim"]
    },
    {
      "use" : "maiden",
      "family" : "Windsor",
      "given" : ["Peter",
      "James"],
      "period" : {
        "end" : "2002"
      }
    }],
    "telecom" : [{
      "use" : "home"
    },
    {
      "system" : "phone",
      "value" : "(03) 5555 6473",
      "use" : "work",
      "rank" : 1
    },
    {
      "system" : "phone",
      "value" : "(03) 3410 5613",
      "use" : "mobile",
      "rank" : 2
    },
    {
      "system" : "phone",
      "value" : "(03) 5555 8834",
      "use" : "old",
      "period" : {
        "end" : "2014"
      }
    }],
    "gender" : "male",
    "birthDate" : "1974-12-25",
    "_birthDate" : {
      "extension" : [{
        "url" : "http://hl7.org/fhir/StructureDefinition/patient-birthTime",
        "valueDateTime" : "1974-12-25T14:35:45-05:00"
      }]
    },
    "deceasedBoolean" : false,
    "address" : [{
      "use" : "home",
      "type" : "both",
      "text" : "534 Erewhon St PeasantVille, Rainbow, Vic  3999",
      "line" : ["534 Erewhon St"],
      "city" : "PleasantVille",
      "district" : "Rainbow",
      "state" : "Vic",
      "postalCode" : "3999",
      "period" : {
        "start" : "1974-12-25"
      }
    }],
    "contact" : [{
      "relationship" : [{
        "coding" : [{
          "system" : "http://terminology.hl7.org/CodeSystem/v2-0131",
          "code" : "N"
        }]
      }],
      "name" : {
        "family" : "du Marché",
        "_family" : {
          "extension" : [{
            "url" : "http://hl7.org/fhir/StructureDefinition/humanname-own-prefix",
            "valueString" : "VV"
          }]
        },
        "given" : ["Bénédicte"]
      },
      "additionalName" : [{
        "use" : "nickname",
        "given" : ["Béné"]
      }],
      "telecom" : [{
        "system" : "phone",
        "value" : "+33 (237) 998327"
      }],
      "address" : {
        "use" : "home",
        "type" : "both",
        "line" : ["534 Erewhon St"],
        "city" : "PleasantVille",
        "district" : "Rainbow",
        "state" : "Vic",
        "postalCode" : "3999",
        "period" : {
          "start" : "1974-12-25"
        }
      },
      "additionalAddress" : [{
        "use" : "work",
        "line" : ["123 Smart St"],
        "city" : "PleasantVille",
        "state" : "Vic",
        "postalCode" : "3999"
      }],
      "gender" : "female",
      "period" : {
        "start" : "2012"
      }
    }],
    "managingOrganization" : {
      "reference" : "Organization/1"
    }
  }