package chap11;

import static chap11.Util.delay;
import static chap11.Util.format;

public class Discount {

    public enum Code {
        NONE(0), SLIVER(5), GOLD(10), PLATINUM(15), DIAMOND(20);

        private final int percentage;

        Code(int percentage) {
            this.percentage = percentage;
        }

        public int getPercentage() {
            return percentage;
        }
    }

    public static String applyDiscount(Quote quote) {
        return String.format("%s price is %.2f.", quote.getShopName(), apply(quote.getPrice(), quote.getDiscountCode()));
    }

    private static double apply(double price, Code code) {
        delay();
        return format(price * (100 - code.percentage) / 100);
    }
}
