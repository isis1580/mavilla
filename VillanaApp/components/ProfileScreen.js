import React from 'react';
import { View, Text, StyleSheet, Image, TouchableOpacity } from 'react-native';
import { FontAwesome, MaterialIcons } from '@expo/vector-icons';
import AppBar from './AppBar';

const ProfileScreen = () => {
  const user = {
    name: 'Nom de l"utilisateur',
    city: 'Niamey',
    job: 'Demarcheur',
    phone: '+22700000',
    email: 'moi@gmail.com',
    socialMedia: {
      facebook: 'https://facebook.com/isis',
      twitter: 'https://twitter.com/isis',
      linkedin: 'https://linkedin.com/isis',
    },
    profileImage: 'https://example.com/user.jpg', // Remplacez par l'URL de l'image de l'utilisateur
  };

  return (
    <View style={styles.container}>
      <AppBar/>
      <View style={styles.header}>
        <TouchableOpacity style={styles.editButton}>
          <MaterialIcons name="edit" size={24} color="#fff" />
        </TouchableOpacity>
        <Image source={require('../assets/profil.jpg')} style={styles.profileImage} />
        <Text style={styles.name}>{user.name}</Text>
      </View>

      <View style={styles.detailsContainer}>
        <Text style={styles.detailItem}>
          <FontAwesome name="map-marker" size={16} color="#444" /> {user.city}
        </Text>
        <Text style={styles.detailItem}>
          <FontAwesome name="briefcase" size={16} color="#444" /> {user.job}
        </Text>
        <Text style={styles.detailItem}>
          <FontAwesome name="phone" size={16} color="#444" /> {user.phone}
        </Text>
        <Text style={styles.detailItem}>
          <FontAwesome name="envelope" size={16} color="#444" /> {user.email}
        </Text>
      </View>

      <View style={styles.socialMediaContainer}>
        <Text style={styles.socialMediaTitle}>Réseaux Sociaux:</Text>
        <View style={styles.socialMediaIcons}>
          <TouchableOpacity onPress={() => { /* Ouvrir Facebook */ }}>
            <FontAwesome name="facebook" size={24} color="#3b5998" />
          </TouchableOpacity>
          <TouchableOpacity onPress={() => { /* Ouvrir Twitter */ }}>
            <FontAwesome name="twitter" size={24} color="#1DA1F2" />
          </TouchableOpacity>
          <TouchableOpacity onPress={() => { /* Ouvrir LinkedIn */ }}>
            <FontAwesome name="linkedin" size={24} color="#0077B5" />
          </TouchableOpacity>
        </View>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#f5f5f5',
  },
  header: {
    alignItems: 'center',
    marginBottom: 20,
    marginTop:50
  },
  editButton: {
    position: 'absolute',
    top: 20,
    right: 20,
    backgroundColor: '#007BFF',
    borderRadius: 20,
    padding: 10,
  },
  profileImage: {
    width: 170,
    height: 170,
    borderRadius: 100,
    marginBottom: 10,
  },
  name: {
    fontSize: 24,
    fontWeight: 'bold',
  },
  detailsContainer: {
    backgroundColor: '#fff',
    borderRadius: 10,
    padding: 15,
    marginBottom: 20,
    elevation: 2,
  },
  detailItem: {
    fontSize: 16,
    marginVertical: 5,
  },
  socialMediaContainer: {
    marginTop: 20,
  },
  socialMediaTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  socialMediaIcons: {
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
});

export default ProfileScreen;