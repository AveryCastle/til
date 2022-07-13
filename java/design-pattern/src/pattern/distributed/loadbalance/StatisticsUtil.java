package pattern.distributed.loadbalance;

public class StatisticsUtil {

    //분산 s^2=[(x1-x)^2 +...(xn-x)^2]/n
    public static double variance(Long[] x) {
        int m = x.length;
        double sum = 0;
        for (int i = 0; i < m; i++) { // 합집합
            sum += x[i];
        }
        double dAve = sum / m; // 평균
        double dVar = 0;
        for (int i = 0; i < m; i++) { // 분산 찾기
            dVar += (x[i] - dAve) * (x[i] - dAve);
        }
        return dVar / m;
    }

    // 표준편차
    public static double standardDeviation(Long[] x) {
        int m = x.length;

        double sum = 0;
        for (int i = 0; i < m; i++) {// 합집합
            sum += x[i];
        }
        double dAve = sum / m;//평균
        double dVar = 0;
        for (int i = 0; i < m; i++) {// 분산 찾기
            dVar += (x[i] - dAve) * (x[i] - dAve);
        }
        return Math.sqrt(dVar / m);
    }
}
