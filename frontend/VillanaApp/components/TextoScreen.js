import React, { useState, useRef, useEffect } from 'react';
import { View, TextInput, Text, Image, StyleSheet, Animated, Keyboard, KeyboardAvoidingView, Platform } from 'react-native';
import FontAwesome from 'react-native-vector-icons/FontAwesome'; 
import { useRoute } from '@react-navigation/native';

const TextoScreen = () => {
  const [messageText, setMessageText] = useState('');
  const inputRef = useRef(null);
  const animation = useRef(new Animated.Value(0)).current; 

  const route = useRoute();
  const { userName, avatarUrl } = route.params;

  useEffect(() => {
    const keyboardDidShowListener = Keyboard.addListener('keyboardDidShow', handleKeyboardShow);
    const keyboardDidHideListener = Keyboard.addListener('keyboardDidHide', handleKeyboardHide);

    return () => {
      keyboardDidShowListener.remove();
      keyboardDidHideListener.remove();
    };
  }, []);

  const handleKeyboardShow = () => {
    Animated.timing(animation, {
      toValue: 1,
      duration: 200,
      useNativeDriver: false,
    }).start();
  };

  const handleKeyboardHide = () => {
    Animated.timing(animation, {
      toValue: 0,
      duration: 200,
      useNativeDriver: false,
    }).start();
  };

  const translateY = animation.interpolate({
    inputRange: [0, 1],
    outputRange: [0, -50], // Ajustez cette valeur
  });

  return (
    <KeyboardAvoidingView 
      style={styles.container} 
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      keyboardVerticalOffset={Platform.OS === 'ios' ? 0 : 0} // Ajustez cette valeur
    >
      <View style={styles.profileContainer}>
        <Image 
          source={require('../assets/profil.jpg')} 
          style={styles.profileImage} 
        />
        <Text style={styles.userName}>{userName}</Text> 
      </View>
      <Animated.View style={[styles.addIconContainer,]}> 
        <View style={styles.viewinput}>
          <FontAwesome name="plus-square-o" size={25} color="green" />
          <TextInput
            ref={inputRef}
            style={styles.input}
            placeholder="Type your message..."
            onChangeText={setMessageText}
            value={messageText}
          />
        </View>
      </Animated.View>
    </KeyboardAvoidingView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1, 
    justifyContent: 'space-between', 
    alignContent: 'center',
  },
  viewinput: {
    marginBottom: 10,
    marginLeft: 10,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  profileContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 10,
    marginTop: 50,
    borderBottomWidth: 1,
    borderBottomColor: '#ccc',
  },
  profileImage: {
    width: 40,
    height: 40,
    borderRadius: 50,
    borderWidth: 1,
    borderColor: '#ccc',
  },
  userName: {
    fontSize: 16,
    marginLeft: 10,
  },
  input: {
    flex: 1,
    height: 40, // Augmentez la hauteur pour plus de confort
    borderRadius: 20,
    paddingHorizontal: 10,
    backgroundColor: '#fff',
    marginHorizontal: 20,
  },
  addIconContainer: {
    borderTopColor: '#000',
    alignItems: 'center',
    backgroundColor: '#ecebe9',
    padding: 10,
    height: 70,
  },
});

export default TextoScreen;