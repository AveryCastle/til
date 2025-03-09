class AppConfig {
  static const String iosClientId = '15020443312-kji0bs11r7ct46gr48mmn796p3o1d5p9.apps.googleusercontent.com';
  static const String androidClientId = 'YOUR-ANDROID-CLIENT-ID.apps.googleusercontent.com';
  
  static String get clientId {
    if (Platform.isIOS) return iosClientId;
    if (Platform.isAndroid) return androidClientId;
    throw UnsupportedError('Unsupported platform');
  }
} 