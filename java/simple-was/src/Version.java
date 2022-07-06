package year2022.wesang;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Version {

    private final Integer major;
    private final Integer minor;
    private final String patch;

    public Version(Integer major, Integer minor, String patch) {
        this.major = major;
        this.minor = minor;
        this.patch = patch;
    }

    static final String PATTERN = "\\d+(\\.\\d+){0,2}(-SNAPSHOT)?";
    static final String errorVersionMustNotBeNull = "'version' must not be null!";
    static final String errorOtherMustNotBeNull = "'other' must not be null!";
    static final String errorVersionMustMatchPattern = "'version' must match: 'major.minor.patch(-SNAPSHOT)'!";

    public Version(String version) {
        if (version == null) throw new IllegalArgumentException(errorVersionMustNotBeNull);
        Pattern pattern = Pattern.compile(PATTERN);
        Matcher matcher = pattern.matcher(version);
        if (!matcher.matches()) {
            throw new IllegalArgumentException(errorVersionMustMatchPattern);
        }

        int count = matcher.groupCount();
        if (count >= 1) {
            this.major = Integer.parseInt(matcher.group());
        }
        if (count >= 2) {
            this.minor = Integer.parseInt(matcher.group());
        }
        if (count >= 3) {
            this.patch = matcher.group();
        }
    }
}
