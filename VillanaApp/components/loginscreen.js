import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  Image,
  TouchableOpacity,
  StyleSheet,
  KeyboardAvoidingView,
  Platform,
  SafeAreaView,
  ScrollView,
  Animated,
  StatusBar 
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import axios from 'axios'; // Importer Axios

export default function LoginScreen({ navigation }) {
  const [emailOrPhone, setEmailOrPhone] = useState(''); // Renommer pour refléter l'utilisation du numéro de téléphone ou de l'email
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [isFocused, setIsFocused] = useState({
    emailOrPhone: false,
    password: false,
  });
  const [iconColor] = useState(new Animated.Value(0));

  const handleLogin = async () => {
    try {
      const response = await axios.post('YOUR_API_ENDPOINT/login/', {
        username: emailOrPhone, // Utiliser le champ approprié
        password: password,
      });
      // Gérer la réponse, par exemple, stocker le token et naviguer vers l'écran d'accueil
      console.log(response.data);
      navigation.navigate('HomeScreen');
    } catch (error) {
      console.error('Erreur lors de la connexion', error);
      // Gérer les erreurs, par exemple, afficher un message d'erreur
    }
  };

  const handleFocus = (field) => {
    setIsFocused((prev) => ({ ...prev, [field]: true }));
  };

  const handleBlur = (field) => {
    setIsFocused((prev) => ({ ...prev, [field]: false }));
  };

  const handlePasswordToggle = () => {
    setShowPassword(!showPassword);
    Animated.sequence([
      Animated.timing(iconColor, { toValue: 1, duration: 200, useNativeDriver: false }),
      Animated.timing(iconColor, { toValue: 0, duration: 200, useNativeDriver: false }),
    ]).start();
  };

  const iconColorInterpolation = iconColor.interpolate({
    inputRange: [0, 1],
    outputRange: ['grey', '#00BFFF']
  });

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="dark-content" />
      <KeyboardAvoidingView
        style={styles.container}
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        keyboardVerticalOffset={Platform.OS === 'ios' ? 0 : 20}
      >
        <ScrollView
          contentContainerStyle={styles.scrollViewContent}
          keyboardShouldPersistTaps="handled"
          showsVerticalScrollIndicator={false}
        >
          <View style={styles.header}>
            <Image
              source={require('../assets/villanaicon.png')}
              style={styles.logo}
            />
            <TouchableOpacity style={styles.skipButton} onPress={() =>navigation.navigate('Accueil')}>
              <Text style={styles.skipButtonText}>Ignorer</Text>
            </TouchableOpacity>
          </View>
          <View style={styles.form}>
            <TextInput
              value={emailOrPhone}
              onChangeText={setEmailOrPhone}
              placeholder="Numéro de Telephone"
              placeholderTextColor="grey"
              style={[styles.input, isFocused.emailOrPhone && styles.inputFocused]}
              onFocus={() => handleFocus('emailOrPhone')}
              onBlur={() => handleBlur('emailOrPhone')}
            />
            <View style={styles.passwordContainer}>
              <TextInput
                value={password}
                onChangeText={setPassword}
                placeholder="Mot de passe"
                placeholderTextColor="grey"
                secureTextEntry={!showPassword}
                style={[styles.input, isFocused.password && styles.inputFocused]}
                onFocus={() => handleFocus('password')}
                onBlur={() => handleBlur('password')}
              />
              <TouchableOpacity
                onPress={handlePasswordToggle}
                style={styles.showPasswordButton}
              >
                <Animated.View>
                <Ionicons name={showPassword ? 'eye-off' : 'eye'} size={20} color={iconColorInterpolation} />
                </Animated.View>
              </TouchableOpacity>
            </View>
            <TouchableOpacity onPress={() => navigation.navigate('UserForm')}>
              <Text style={styles.forgotPasswordText}>Mot de passe oublié ?</Text>
            </TouchableOpacity>
            
            <TouchableOpacity
              onPress={handleLogin}
              style={styles.loginButton}
            >
              <Text style={styles.loginButtonText}>Se Connecter</Text>
            </TouchableOpacity>
            <TouchableOpacity
              style={styles.googleButton}
              onPress={() => navigation.navigate('GoogleLogin')}
            >
              <Image
                source={require('../assets/google_logo.png')}
                style={styles.googleLogo}
              />
              <Text style={styles.googleButtonText}>Se connecter avec Google</Text>
            </TouchableOpacity>
          </View>
        </ScrollView>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: 'white',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginTop: 70, // Ajustez si nécessaire
    paddingHorizontal: 16,
  },
  skipButton: {
    backgroundColor: '#0F4C81',
    paddingVertical: 8,
    paddingHorizontal: 16,
    borderRadius: 8,
  },
  skipButtonText: {
    color: 'white',
    fontSize: 16,
  },
  logo: {
    height: 60,
    width: 140,
    resizeMode: 'contain',
  },
  form: {
    paddingHorizontal: 26,
    paddingTop: 0,
    flex: 1,
    justifyContent: 'center',
  },
  scrollViewContent: {
    flexGrow: 1,
  },
  input: {
    color: 'black',
    borderColor: 'grey',
    borderWidth: 1,
    borderRadius: 8,
    marginBottom: 16,
    padding: 12,
    fontSize: 16,
    width: '100%',
  },
  inputFocused: {
    borderColor: '#0F4C81',
  },
  passwordContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 16,
    position: 'relative',
  },
  showPasswordButton: {
    position: 'absolute',
    right: 10,
    top: '50%',
    transform: [{ translateY: -10 }],
  },
  forgotPasswordText: {
    color: 'grey',
    textAlign: 'left',
    marginVertical: 8,
  },
  loginButton: {
    backgroundColor: '#0F4C81',
    borderRadius: 8,
    padding: 16,
    alignItems: 'center',
    marginTop: 32,
  },
  InscriptionButton: {
    width:100,
    backgroundColor: '#0F4C81',
    borderRadius: 8,
    padding: 10,
    alignItems: 'center',
    marginTop: 32,
    justifyContent:'flex-start'
  },
  loginButtonText: {
    color: 'white',
    fontSize: 18,
  },
  googleButton: {
    flexDirection: 'row',
    backgroundColor: 'rgba(255, 255, 255, 0.8)',
    borderRadius: 8,
    padding: 16,
    alignItems: 'center',
    marginTop: 16,
    justifyContent: 'center',
  },
  googleLogo: {
    height: 24,
    width: 24,
    resizeMode: 'contain',
  },
  googleButtonText: {
    color: 'black',
    fontSize: 18,
    marginLeft: 8,
  },
});
