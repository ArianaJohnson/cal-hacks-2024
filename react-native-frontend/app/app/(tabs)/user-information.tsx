import React, { useState } from 'react';
import { StyleSheet, TextInput, Button, ScrollView, Image, ImageBackground, View } from 'react-native';
import { Text } from '@/components/Themed';

export default function TabTwoScreen() {
  const [name, setName] = useState('');
  const [age, setAge] = useState('');
  const [gender, setGender] = useState('');
  const [emergencyContactName, setEmergencyContactName] = useState('');
  const [emergencyContactPhone, setEmergencyContactPhone] = useState('');
  const [medicalConditions, setMedicalConditions] = useState('');
  const [allergies, setAllergies] = useState('');
  const [medications, setMedications] = useState('');

  const handleSubmit = () => {
    const patientData = {
      name,
      age: isNaN(parseInt(age)) ? null : parseInt(age),
      gender,
      emergency_contact: {
        name: emergencyContactName,
        phone: emergencyContactPhone,
      },
      medical_info: {
        medical_conditions: medicalConditions.split(','),
        allergies: allergies ? allergies.split(',') : [],
        medications: medications ? medications.split(',') : [],
      },
    };
    console.log(patientData); // You can send this data to your FastAPI backend
  };

  return (
    <ScrollView contentContainerStyle={[styles.container, { backgroundColor: 'white' }]}>

      <Image
        source={require('./guardian_angels_bear.png')}  // Ensure the path is correct
        style={styles.guardianAngel}
      />

      <Image
        source={require('./patient information form.png')}  // Ensure the path is correct
        style={styles.patientInfoForm}
      />

      {/* Wrap each TextInput in ImageBackground */}
      {renderInputField("Name", name, setName)}
      {renderInputField("Age", age, setAge, { keyboardType: "numeric" })}
      {renderInputField("Gender", gender, setGender)}
      {renderInputField("Emergency Contact Name", emergencyContactName, setEmergencyContactName)}
      {renderInputField("Emergency Contact Phone", emergencyContactPhone, setEmergencyContactPhone, { keyboardType: "phone-pad" })}
      {renderInputField("Medical Conditions (comma-separated)", medicalConditions, setMedicalConditions)}
      {renderInputField("Allergies (comma-separated, optional)", allergies, setAllergies)}
      {renderInputField("Medications (comma-separated, optional)", medications, setMedications)}

      <Button title="Submit" onPress={handleSubmit} />

    </ScrollView>
  );
}

// Function to render the input fields with ImageBackground
const renderInputField = (label, value, onChangeText, additionalProps = {}) => (
  <View style={styles.inputFieldContainer}>
    <Text style={styles.label}>{label}</Text>
    <ImageBackground
      source={require('./backgroundImage.png')} // Replace with your image path
      style={styles.inputBackground}
      imageStyle={styles.imageStyle} // Optional, for styling the image
    >
      <TextInput
        style={styles.input}
        placeholder={`Enter ${label.toLowerCase()}`}
        value={value}
        onChangeText={onChangeText}
        {...additionalProps} // Spread additional props like keyboardType
      />
    </ImageBackground>
  </View>
);

const styles = StyleSheet.create({
  container: {
    padding: 20,
    flexGrow: 1,
  },
  guardianAngel: {
    width: 200,
    height: 200,
    alignSelf: 'center',
    resizeMode: 'contain',
    marginBottom: 10,
  },
  patientInfoForm: {
    width: 350,
    height: 350,
    alignSelf: 'center',
    resizeMode: 'contain',
    marginBottom: -150,
    marginTop: -170,
  },
  inputFieldContainer: {
    marginBottom: 15, // Space between input fields
  },
  inputBackground: {
    width: '100%',
    height: 50, // Increased height for more background visibility
    justifyContent: 'center', // Center the input vertically
    marginBottom: 10,
    borderRadius: 5,
    overflow: 'hidden', // To clip the edges of the background
  },
  label: {
    width: '100%',
    textAlign: 'left',
    marginBottom: 5,
    fontSize: 16,
    fontWeight: '600',
    fontFamily: 'NewsReader',
  },
  input: {
    height: '100%', // Fill the entire height of the background
    paddingHorizontal: 10,
    paddingVertical: 15, // Increased padding for more space
    color: 'white', // Change text color
  },
  imageStyle: {
    borderRadius: 5, // Match the input's border radius
  },
});
