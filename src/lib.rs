use pyo3::prelude::*;

#[pyfunction]
pub fn add(left: u64, right: u64) -> u64 {
  left + right
}

pub fn subtract(left: u64, right: u64) -> u64 {
  left - right
}

#[pymodule]
#[pyo3(name = "_libxiangqi")]
fn _libxiangqi(m: &Bound<'_, PyModule>) -> PyResult<()> {
  m.add_function(wrap_pyfunction!(add, m)?)?;
  Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_works() {
        let result = add(2, 2);
        assert_eq!(result, 4);
    }
}
