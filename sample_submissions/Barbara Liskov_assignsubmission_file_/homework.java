/******************************************************************************
 *
 *  Description:  Includes a few utility functions useful for working with
 *  arrays (implemented with loops).
 *
 ******************************************************************************/

public class LoopUtils {

  // Find the max element of an array
  public static int max(int[] arr) {
    int x = 0;


    for (int i = 0; i < arr.length; i++) {
      if (arr[i] > x) {

        x = arr[i];

      }
    }

    return x;
  }
}